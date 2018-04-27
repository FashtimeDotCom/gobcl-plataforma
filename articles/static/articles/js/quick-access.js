/**
 * JQuery Plugin (Quick access for article plugins.).
 *
 * jQuery lightweight plugin boilerplate from: @addyosmani
 */
(function ($) {

  var pluginName = 'quickAccess';
  var pluginDataKey = 'quickAccessInstance';

  var pluginsData = [
    { icon: 'fa-table', pluginType: 'GalleryCMSPlugin' },
    { icon: 'fa-twitter', pluginType: 'HtmlCMSPlugin' },
    { icon: 'fa-picture-o', pluginType: 'PicturePlugin' },
    { icon: 'fa-link', pluginType: 'LinkPlugin' },
    { icon: 'fa-font', pluginType: 'TextPlugin' },
    { icon: 'fa-video-camera', pluginType: 'VideoPlayerPlugin' }
  ];

  var defaults = {};

  function Plugin(element, options) {
    this.$element = $(element);

    this.options = $.extend({}, defaults, options, this.$element.data());
    this.$toolbox = this._makeToolBox();

    this.init();
  }

  Plugin.prototype.init = function () {
    var that = this;

    this._addToolBoxListener();
    this.plugins = this._getPluginsMap();

    if ($('.editor-zone').length) {
      that.$element.append(that.$toolbox.clone(true).data('before', true));
    }

    Object.keys(this.plugins).forEach(function (id, index) {
      var block = $('<div/>', { class: 'plugin-block plugin-block-' + id })
        .data('cms', that.plugins[id]);

      $('.cms-plugin-' + id).appendTo(block);

      block.append(that.$toolbox.clone(true).data('before', false));
      that.$element.append(block);
    });
  };

  Plugin.prototype._getPluginsMap = function () {
    return this.$element
      .find('.cms-plugin')
      .map(function (index, plugin) {
        return $(plugin).data('cms')[0];
      })
      .toArray()
      .reduce(function (current, data) {
        current[data.plugin_id] = data;
        return current;
      }, {});
  };

  Plugin.prototype._addToolBoxListener = function () {
    var that = this;

    $(this.$element).on('click', '.plugin-block-actions .btn', function () {
      var $pluginBlock = $(this).closest('.plugin-block');

      var position = $pluginBlock.index();

      that.options.onToolClick(
        pluginsData[parseInt($(this).data('index'))],
        that.$element.children('.cms-placeholder').data('cms'),
        position < 0 ? 0 : position
      )
    });
  };

  Plugin.prototype._makeToolBox = function () {
    var $actions = $('<div/>', { class: 'plugin-block-actions text-center py-3'});

    var $group = $('<div/>', { class: 'btn-group' });

    for (var i = 0; i < pluginsData.length; i += 1) {
      var pluginData = pluginsData[i];
      $group.append(
        $('<button/>', { type: 'button', class: 'btn btn-white'})
          .append($('<i/>', { class: 'fa ' + pluginData.icon }))
          .data('index', i)
      );
    }

    $actions.append($group);

    return $actions;
  };

  Plugin.prototype.update = function () {

  };

  Plugin.prototype.setOptions = function (options) {
    this.options = $.extend(this.options, options, this.$element.data());
    this.update();
  };

  $.fn[pluginName] = function (options) {
    return this.each(function () {
      if (!$.data(this, pluginDataKey)) {
        $.data(this, pluginDataKey, new Plugin(this, options));
      } else {
        $.data(this, pluginDataKey).setOptions(options);
      }
    });
  };

  $(function () {
    console.log('aca');
    $('.editor-zone').quickAccess({
      onToolClick: function (pluginData, placeholderData, position) {

        var plugin = new CMS.Plugin(
          placeholderData.placeholder_id,
          placeholderData
        );

        plugin.addPlugin(pluginData.pluginType, 'New Plugin');
      }
    });
  });

})(CMS.$);

