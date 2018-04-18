/**
 * JQuery Plugin (Quick access for article plugins.).
 *
 * jQuery lightweight plugin boilerplate from: @addyosmani
 */
(function ($) {


  var pluginName = 'quickAccess';
  var pluginDataKey = 'quickAccessInstance';

  var defaults = {};

  function Plugin(element, options) {
    this.$element = $(element);

    this.options = $.extend({}, defaults, options, this.$element.data());

    this.init();
  }

  Plugin.prototype.init = function () {
    var that = this;

    $(this.$element).on('click', '.plugin-block-actions .btn', function () {
      that.options.onToolClick(
        $(this).data('tool'),
        $(this).closest('.plugin-block').data('cms'),
        $(this).closest('.plugin-block-actions').data('before')
      )
    });

    this.plugins = this.$element
      .find('.cms-plugin')
      .map(function (index, plugin) {
        return $(plugin).data('cms')[0];
      })
      .toArray()
      .reduce(function (current, data) {
        current[data.plugin_id] = data;
        return current;
      }, {});

    Object.keys(this.plugins).forEach(function (id, index) {
      var block = $('<div/>', { class: 'plugin-block plugin-block-' + id })
        .data('cms', that.plugins[id]);

      if (index === 0) {
        block.append(that._makeToolBox(true));
      }

      $('.cms-plugin-' + id).appendTo(block);

      block.append(that._makeToolBox(false));
      that.$element.append(block);
    });
  };

  Plugin.prototype._makeToolBox = function (before) {
    return $('<div/>', { class: 'plugin-block-actions text-center py-3'}).append(
      $('<div/>', { class: 'btn-group' }).append(
        $('<button/>', { type: 'button', class: 'btn btn-white'})
          .append($('<i/>', { class: 'fa fa-picture-o' }))
          .data('tool', 'picture'),
        $('<button/>', { type: 'button', class: 'btn btn-white'})
          .append($('<i/>', { class: 'fa fa-font' }))
          .data('tool', 'text'),
        $('<button/>', { type: 'button', class: 'btn btn-white'})
          .append($('<i/>', { class: 'fa fa-link' }))
          .data('tool', 'link'),
        $('<button/>', { type: 'button', class: 'btn btn-white'})
          .append($('<i/>', { class: 'fa fa-video-camera' }))
          .data('tool', 'video')
      )
    ).data('before', before);
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
    $('.editor-zone').quickAccess({
      onToolClick: function (toolType, plugin, before) {
        console.log(toolType);
        console.log(plugin);
        console.log(before);
      }
    });
  });

})(CMS.$);

