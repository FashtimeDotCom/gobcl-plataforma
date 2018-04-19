/**
 * JQuery Plugin (Quick access for article plugins.).
 *
 * jQuery lightweight plugin boilerplate from: @addyosmani
 */
(function ($) {

  var pluginName = 'quickAccess';
  var pluginDataKey = 'quickAccessInstance';

  var pluginsData = [{
    icon: 'fa-table',
    defaults: {
      description: 'Descripción galería'
    },
    pluginType: 'GalleryCMSPlugin'
  }, {
    icon: 'fa-twitter',
    defaults: {
      html: '<p>Colocar iframe acá</p>'
    },
    pluginType: 'HtmlCMSPlugin'

  }, {
    icon: 'fa-picture-o',
    defaults: {
      external_picture: 'http://www.lacronicavirtual.com/blogs/viajealosandes/wp-content/uploads/DSCF1559.jpg',
      '_popup': '1',
      template: 'default',
      initialatributes: '{}',
      link_page_0: '1',
      initiallik_attributes: '{}',
      use_automatic_scaling: 'on'
    },
    pluginType: 'PicturePlugin'

  }, {
    icon: 'fa-link',
    defaults: {
      '_popup': '1',
      external_link: 'https://prensa.presidencia.cl/',
      internal_link_0: '1',
      name: 'Link',
      template: 'default'
    },
    pluginType: 'LinkPlugin'

  }, {
    icon: 'fa-font',
    defaults: {
      '_popup': '1',
      body: '<p>Hola que tal</p>\r\n'
    },
    pluginType: 'TextPlugin',
    url: '/admin/cms/page/add-plugin/'

  }, {
    icon: 'fa-video-camera',
    defaults: {
      '_popup': '1',
      template: 'default',
      label: '',
      embed_link: 'https://www.youtube.com/watch?v=DXzAHhfytoo&feature=youtu.be',
      poster: ''
    },
    pluginType: 'VideoPlayerPlugin'
  }];

  var defaults = {};

  function Plugin(element, options) {
    this.$element = $(element);

    this.options = $.extend({}, defaults, options, this.$element.data());

    this.init();
  }

  Plugin.prototype.init = function () {
    var that = this;

    $(this.$element).on('click', '.plugin-block-actions .btn', function () {
      var $pluginBlock = $(this).closest('.plugin-block');

      var position = $pluginBlock.index();

      if (position < 0) {
        position = 0;
      }

      that.options.onToolClick(
        pluginsData[parseInt($(this).data('index'))],
        $(this).closest('.plugin-block').data('cms'),
        position
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

    if ($('.editor-zone').length) {
      that.$element.append(that._makeToolBox(true));
    }

    Object.keys(this.plugins).forEach(function (id, index) {
      var block = $('<div/>', { class: 'plugin-block plugin-block-' + id })
        .data('cms', that.plugins[id]);

      $('.cms-plugin-' + id).appendTo(block);

      block.append(that._makeToolBox(false));
      that.$element.append(block);
    });
  };

  Plugin.prototype._makeToolBox = function (before) {
    var $div = $('<div/>', { class: 'plugin-block-actions text-center py-3'});

    for (var i = 0; i < pluginsData.length; i += 1) {
      var pluginData = pluginsData[i];

      $div.append($('<div/>', { class: 'btn-group' }).append(
        $('<button/>', { type: 'button', class: 'btn btn-white'})
          .append($('<i/>', { class: 'fa ' + pluginData.icon }))
          .data('tool', pluginData.pluginType)
          .data('index', i)
      ))
    }

    $div.data('before', before);
    return $div;
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
      onToolClick: function (pluginData, parentPlugin, position) {
        var url;
        var placeholderId;

        if (pluginData.url) {
          url = pluginData.url;
        } else {
          url = '/admin/articles/article/add-plugin/';
        }

        if (parentPlugin) {
          placeholderId = parentPlugin.placeholder_id;
        } else {
          placeholderId = App.placeholderId;
        }
        var params = {
          cms_path: location.pathname,
          placeholder_id: placeholderId,
          plugin_language: App.currentLanguage,
          plugin_type: pluginData.pluginType,
          plugin_position: position
        };

        url = url + '?' +  $.param(params);

        var data = $.extend(
          {csrfmiddlewaretoken: App.csrftoken, plugin_position: position},
          pluginData.defaults
        );

        $.post(url, data, function(data, textStatus, jqXHR) {
          window.location.reload();
        });
      }
    });
  });

})(CMS.$);

