(function ($) {

  $(function () {

    $('.cms-plugin').on('dblclick', function (e) {
      var data = $(this).data('cms')[0];

      if (data.plugin_type === 'TextPlugin') {
        e.stopPropagation();
        e.preventDefault();

        var $container = CMS.$('<div/>');

        // iFrame
        var $iFrame = $('<iframe/>', {
            tabindex: 0,
            src: data.urls.edit_plugin,
            class: 'w-100',
            frameborder: 0,
            style: 'height: 400px'
          });


        $iFrame.on('load', function () {

          var $row = $iFrame.contents().find('.submit-row:eq(0)');
          var $form = $iFrame.contents().find('form');
          var $group = $('<div/>', { class: 'cms-modal-item-buttons' });
          var $actions = $('<div/>', { class: 'cms-modal-buttons-inner' });
          var $cancel = $('<a/>', {
            href: '#',
            class: 'cms-btn'
          })
            .html(CMS.config.lang.cancel);

          console.log($iFrame.contents().find('head'));

          console.log($('#gobStyle'));

          $iFrame.contents().find('head').append($('#gobStyle').clone());

          $form.on('submit', function () {
            // TODO: hide iframe and reload view or show content.
          });

          var $buttons = $row.find('input, a, button');

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
              .on('click.cms.modal touchend.cms.modal', function (e) {
                e.preventDefault();

                if ($item.hasClass('default') || $item.hasClass('deletelink')) {
                  // TODO: hide iframe and reload view or show content.
                }

                if ($item.is('input') || $item.is('button')) {
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

          $cancel.on('click.cms.modal', function (e) {
            e.preventDefault();
            // TODO: hide iframe and reload view or show content.
          });

          $cancel.wrap($group);
          $actions.append($cancel.parent());


          $actions.find('.cms-btn-group').unwrap();
          var tmp = $actions.find('.cms-btn-group').clone(true, true);
          $actions.find('.cms-btn-group').remove();
          $actions.append(tmp.wrapAll($group.clone().addClass('cms-modal-item-buttons-left')).parent());

          $container.append($actions);

        });

        $container.append($iFrame);
        $(this).append($container);

      }
    })
  });

})(CMS.$);