/**
 * Enable inline edition in articles.
 */
(function ($) {

  var Loader = (function () {

    NProgress.configure({
      showSpinner: false,
      parent: '#cms-top',
      trickleSpeed: 200,
      minimum: 0.3,
      template: '<div class="cms-loading-bar" role="bar">' +
        '<div class="cms-loading-peg"></div>' +
      '</div>'
    });

    return {
      showLoader: _.debounce(function () {
        NProgress.start();
      }, 0),
      hideLoader: function () {
        this.showLoader.cancel();
        NProgress.done();
      }
    }

  })();


  var Editor = (function () {

    function Editor(options) {
      this.options = $.extend(true, {}, Editor.options, options);

      this.click = 'click.cms.modal';
      this.doubleClick = 'dblclick.cms.modal';
      this.touchEnd = 'touchend.cms.modal';
      this.saved = false;

      this._setupUI();
      // TODO before unload handler
    }

    Editor.prototype._setupUI = function () {

      this.ui = {
        $plugins: $('.cms-plugin-' + this.options.plugin_id),
        $container: $('<div/>', { id: this.options.plugin_id, class: 'frame w-100 cms position-relative' }),
        $frame: $('<div/>', { class: 'frame-container w-100' }),
        $actions: $('<div/>', { class: 'frame-actions clearfix w-100'})
      };

      this.ui.$container.append(this.ui.$frame, this.ui.$actions);
      this.ui.$container.insertBefore(this.ui.$plugins[0]);
    };

    Editor.prototype.open = function () {

      this._loadIframe({
        url: this.options.urls.edit_plugin,
        title: 'temp'
      });

      return this;
    };

    Editor.prototype._loadIframe = function (opts) {
      var that = this;
      var SHOW_LOADER_TIMEOUT = 500;

      opts.url = CMS.API.Helpers.makeURL(opts.url);
      opts.title = opts.title || '';

      Loader.showLoader();

      var $holder = this.ui.$frame;
      var $iFrame = $('<iframe/>', {
        tabindex: 0,
        src: opts.url,
        class: 'w-100',
        frameborder: 0,
        zIndex: 'unset'
      })
        .css({
          height: this._calculateHeight(),
          minHeight: 260,
          maxHeight: document.documentElement.clientHeight - 180,
          visibility: 'hidden'
        });

      $holder.css('visibility', 'hidden');

      var loaderTimeout = setTimeout(function () {
        that.ui.$container.addClass('cms-loader')
      }, SHOW_LOADER_TIMEOUT);

      $iFrame.on('load', function () {
        clearTimeout(loaderTimeout);

        var $contents;
        var $body;
        var $messageList;
        var messages;

        try {
          $contents = $iFrame.contents();
          $body = $contents.find('body');
        } catch (error) {
          CMS.API.Messages.open({
            message: '<strong>' + CMS.config.lang.errorLoadingEditForm + '</strong>',
            error: true,
            delay: 0
          });
          that.close();
          return;
        }

        if ($iFrame[0].contentWindow && $iFrame[0].contentWindow.CMS && $iFrame[0].contentWindow.CMS.CKEditor) {
          $($iFrame[0].contentWindow.document).ready(function() {

            setTimeout(function () {
              var editor = $iFrame[0].contentWindow.CMS.CKEditor.editor;

              if (editor) {
                editor.on('instanceReady', function(e) {
                  var $ckEditorIframe = $(e.editor.container.$).find('iframe');

                  $ckEditorIframe
                    .contents()
                    .find('head')
                    .append($('#gobstyle').children('link').clone());

                  $ckEditorIframe
                    .contents()
                    .find('body')
                    .addClass('main-post');

                });
              }
            }, 100);

          });
        }

        var saveSuccess = Boolean($contents.find('.messagelist :not(".error")').length);

        if (!saveSuccess) {
          saveSuccess =
            Boolean($contents.find('.dashboard #content-main').length) &&
            !$contents.find('.messagelist .error').length;
        }

        $messageList = $contents.find('.messagelist');
        messages = $messageList.find('li');

        if (messages.length) {
          CMS.API.Messages.open({
            message: messages.eq(0).html()
          });
        }
        $messageList.remove();

        $body.addClass('cms-admin cms-admin-modal');

        that.ui.$container.removeClass('cms-loader');
        Loader.hideLoader();

        if (messages.length && that.enforceReload) {
          that.ui.modalBody.addClass('cms-loader');
          Loader.showLoader();
          CMS.API.Helpers.reloadBrowser();
        }
        if (messages.length && that.enforceClose) {
          that.close();
          return false;
        }

        $contents.find('.viewsitelink').attr('target', '_top');

        that._setButtons($(this));

        if (
          $contents.find('.errornote').length ||
          $contents.find('.errorlist').length ||
          (that.saved && !saveSuccess)
        ) {
          that.saved = false;
        }

        if (that.saved && saveSuccess && !$contents.find('.delete-confirmation').length) {
          that.ui.$container.addClass('cms-loader');
          if (that.options.onClose) {

            Loader.showLoader();
            CMS.API.Helpers.reloadBrowser(
              that.options.onClose ? that.options.onClose : window.location.href,
              false,
              true
            );
          } else {
            setTimeout(function () {
              if (that.justDeleted && (that.justDeletedPlugin || that.justDeletedPlaceholder)) {

                // TODO load this function
                /*CMS.API.StructureBoard.invalidateState(
                  that.justDeletedPlaceholder ? 'CLEAR_PLACEHOLDER' : 'DELETE',
                  {
                    plugin_id: that.justDeletedPlugin,
                    placeholder_id: that.justDeletedPlaceholder,
                    deleted: true
                  }
                );*/
              }

              that.close();
            }, 150);
          }
        } else {
          $iFrame
            .show()
            .css('visibility', 'visible')
            .data('ready', true);

          $holder.css('visibility', 'visible');
        }
      });
      $holder.html($iFrame);
      this.ui.$plugins.addClass('d-none');
    };

    Editor.prototype._setButtons = function ($iFrame) {
      var djangoSuit = $iFrame.contents().find('.suit-columns').length > 0;

      var that = this;
      var $row;
      var $form = $iFrame.contents().find('form');
      var $group = $('<div/>', { class: 'cms-modal-item-buttons' });
      var $actions = $('<div/>', { class: 'cms-modal-buttons-inner' });
      var $cancel = $('<a/>', {
        href: '#',
        class: 'cms-btn'
      })
        .html(CMS.config.lang.cancel);

      if (djangoSuit) {
        $row = $iFrame.contents().find('.save-box:eq(0)');
      } else {
        $row = $iFrame.contents().find('.submit-row:eq(0)');
      }

      $form.on('submit', function () {
        if (that.hideFrame) {
          that.ui.$frame.find('iframe').hide();
          that.saved = true;
        }
      });

      var $buttons = $row.find('input, a, button');

      $buttons.on('click', function() {
        if ($(this).hasClass('default')) {
          that.hideFrame = true;
        }
      });

      $iFrame.contents().find('.submit-row').hide();

      if (!$buttons.length) {
        $row = $iFrame.contents().find('body:not(.change-list) #content form:eq(0)');
        $buttons = $row.find('input[type="submit"], button[type="submit"]');
        $buttons.addClass('deletelink').hide();
      }

      $buttons.each(function (index, button) {
        var $item = $(button);

        $item.attr('data-rel', '_' + index);

        if ($item.attr('type') === 'hidden') {
          return false;
        }

        var title = $item.attr('value') || $item.text();
        var cls = 'cms-btn';

        if ($item.is('button')) {
          title = $item.text();
        }

        if ($item.hasClass('default')) {
          cls = 'cms-btn cms-btn-action';
        }

        if ($item.hasClass('deletelink')) {
          cls = 'cms-btn cms-btn-caution';
        }

        var $el = $('<a/>', {
          href: '#',
          class: cls + ' ' + $item.attr('class')
        })
          .html(title)
          .on(that.click + ' ' + that.touchEnd, function (e) {
            e.preventDefault();

            if ($item.is('a')) {
              console.log(CMS.API.Helpers.updateUrlWithPath($item.prop('href')));
              that._loadIframe({
                url: CMS.API.Helpers.updateUrlWithPath($item.prop('href')),
                name: title
              });
            }

            if ($item.hasClass('default') || $item.hasClass('deletelink')) {
              if ($item.hasClass('default')) {
                that.hideFrame = true;
              } else {
                that.ui.$frame.find('iframe').hide();
                that.saved = true;

                if ($item.hasClass('deletelink')) {
                  that.justDeleted = true;

                  var action = $item.closest('form').prop('action');

                  if (action.match(/delete-plugin/)) {
                    that.justDeletedPlugin = /delete-plugin\/(\d+)\//gi.exec(action)[1];
                  }
                  if (action.match(/clear-placeholder/)) {
                    that.justDeletedPlaceholder = /clear-placeholder\/(\d+)\//gi.exec(action)[1];
                  }
                }
              }
            }

            if ($item.is('input') || $item.is('button')) {
              that.ui.$container.addClass('cms-loader');
              var $form = $item.closest('form');

              // In Firefox with 1Password extension installed (FF 45 1password 4.5.6 at least)
              // the item[0].click() doesn't work, which notably breaks
              // deletion of the plugin. Workaround is that if the clicked button
              // is the only button in the form - submit a form, otherwise
              // click on the button
              if ($form.find('button, input[type="button"], input[type="submit"]').length > 1) {
                // we need to use native `.click()` event specifically
                // as we are inside an iframe and magic is happening
                $item[0].click();
              } else {
                // have to dispatch native submit event so all the submit handlers
                // can be fired, see #5590
                var event = document.createEvent('HTMLEvents');

                event.initEvent('submit', false, true);
                if ($form[0].dispatchEvent(event)) {
                  // triggering submit event in webkit based browsers won't
                  // actually submit the form, while in Gecko-based ones it
                  // will and calling frm.submit() would throw NS_ERROR_UNEXPECTED
                  try {
                    $form[0].submit();
                  } catch (err) {}
                }
              }
            }
          });

        $el.wrap($group);
        $actions.append($el.parent());

      });

      $cancel.on(that.click, function (e) {
        e.preventDefault();
        that._cancelHandler();
      });

      $cancel.wrap($group);
      $actions.append($cancel.parent());


      $actions.find('.cms-btn-group').unwrap();
      var tmp = $actions.find('.cms-btn-group').clone(true, true);
      $actions.find('.cms-btn-group').remove();
      $actions.append(tmp.wrapAll($group.clone().addClass('cms-modal-item-buttons-left')).parent());

      that.ui.$actions.html($actions);
    };

    Editor.prototype._cancelHandler = function () {
      this.ui.$plugins.removeClass('d-none');
      this.ui.$container.remove();
    };

    Editor.prototype.close = function () {
      this.ui.$container.remove();
    };

    Editor.prototype._calculateHeight = function () {

      return this.ui.$plugins.map(function (index, plugin) {
        return $(plugin).height() + parseInt($(plugin).css('margin-bottom'), 10);
      })
        .toArray()
        .reduce(function (current, next) {
          return current + next;
        }, 0)
        + 141 // ckeditor controls heights
        + 46 // ckeditor options
        + 44; // blockquote margin bottom.
    };

    Editor.options = {
      transitionDuration: 200
    };

    return Editor;
  })();



  $(function () {
    $('.cms-plugin').on('dblclick', function (e) {
      var data = $(this).data('cms')[0];

      if (data.plugin_type === 'TextPlugin') {
        e.stopPropagation();
        e.preventDefault();

        new Editor(data).open();
      }
    })
  });

})(CMS.$);