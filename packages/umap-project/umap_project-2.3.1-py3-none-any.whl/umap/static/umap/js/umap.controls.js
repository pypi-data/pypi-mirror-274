U.BaseAction = L.ToolbarAction.extend({
  initialize: function (map) {
    this.map = map
    if (this.options.label) {
      this.options.tooltip = this.map.help.displayLabel(
        this.options.label,
        (withKbdTag = false)
      )
    }
    this.options.toolbarIcon = {
      className: this.options.className,
      tooltip: this.options.tooltip,
    }
    L.ToolbarAction.prototype.initialize.call(this)
    if (this.options.helpMenu && !this.map.helpMenuActions[this.options.className])
      this.map.helpMenuActions[this.options.className] = this
  },
})

U.ImportAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'upload-data dark',
    label: 'IMPORT_PANEL',
  },

  addHooks: function () {
    this.map.importer.open()
  },
})

U.EditLayersAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'umap-control-browse dark',
    tooltip: L._('Manage layers'),
  },

  addHooks: function () {
    this.map.editDatalayers()
  },
})

U.EditCaptionAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'umap-control-caption dark',
    tooltip: L._('Edit map name and caption'),
  },

  addHooks: function () {
    this.map.editCaption()
  },
})

U.EditPropertiesAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'update-map-settings dark',
    tooltip: L._('Map advanced properties'),
  },

  addHooks: function () {
    this.map.edit()
  },
})

U.ChangeTileLayerAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'dark update-map-tilelayers',
    tooltip: L._('Change tilelayers'),
  },

  addHooks: function () {
    this.map.updateTileLayers()
  },
})

U.UpdateExtentAction = U.BaseAction.extend({
  options: {
    className: 'update-map-extent dark',
    tooltip: L._('Save this center and zoom'),
  },

  addHooks: function () {
    this.map.updateExtent()
  },
})

U.UpdatePermsAction = U.BaseAction.extend({
  options: {
    className: 'update-map-permissions dark',
    tooltip: L._('Update permissions and editors'),
  },

  addHooks: function () {
    this.map.permissions.edit()
  },
})

U.DrawMarkerAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'umap-draw-marker dark',
    label: 'DRAW_MARKER',
  },

  addHooks: function () {
    this.map.startMarker()
  },
})

U.DrawPolylineAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'umap-draw-polyline dark',
    label: 'DRAW_LINE',
  },

  addHooks: function () {
    this.map.startPolyline()
  },
})

U.DrawPolygonAction = U.BaseAction.extend({
  options: {
    helpMenu: true,
    className: 'umap-draw-polygon dark',
    label: 'DRAW_POLYGON',
  },

  addHooks: function () {
    this.map.startPolygon()
  },
})

U.AddPolylineShapeAction = U.BaseAction.extend({
  options: {
    className: 'umap-draw-polyline-multi dark',
    tooltip: L._('Add a line to the current multi'),
  },

  addHooks: function () {
    this.map.editedFeature.editor.newShape()
  },
})

U.AddPolygonShapeAction = U.AddPolylineShapeAction.extend({
  options: {
    className: 'umap-draw-polygon-multi dark',
    tooltip: L._('Add a polygon to the current multi'),
  },
})

U.BaseFeatureAction = L.ToolbarAction.extend({
  initialize: function (map, feature, latlng) {
    this.map = map
    this.feature = feature
    this.latlng = latlng
    L.ToolbarAction.prototype.initialize.call(this)
    this.postInit()
  },

  postInit: function () {},

  hideToolbar: function () {
    this.map.removeLayer(this.toolbar)
  },

  addHooks: function () {
    this.onClick({ latlng: this.latlng })
    this.hideToolbar()
  },
})

U.CreateHoleAction = U.BaseFeatureAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-new-hole',
      tooltip: L._('Start a hole here'),
    },
  },

  onClick: function (e) {
    this.feature.startHole(e)
  },
})

U.ToggleEditAction = U.BaseFeatureAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-toggle-edit',
      tooltip: L._('Toggle edit mode (⇧+Click)'),
    },
  },

  onClick: function (e) {
    if (this.feature._toggleEditing) {
      this.feature._toggleEditing(e) // Path
    } else {
      this.feature.edit(e) // Marker
    }
  },
})

U.DeleteFeatureAction = U.BaseFeatureAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-delete-all',
      tooltip: L._('Delete this feature'),
    },
  },

  postInit: function () {
    if (!this.feature.isMulti())
      this.options.toolbarIcon.className = 'umap-delete-one-of-one'
  },

  onClick: function (e) {
    this.feature.confirmDelete(e)
  },
})

U.DeleteShapeAction = U.BaseFeatureAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-delete-one-of-multi',
      tooltip: L._('Delete this shape'),
    },
  },

  onClick: function (e) {
    this.feature.enableEdit().deleteShapeAt(e.latlng)
  },
})

U.ExtractShapeFromMultiAction = U.BaseFeatureAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-extract-shape-from-multi',
      tooltip: L._('Extract shape to separate feature'),
    },
  },

  onClick: function (e) {
    this.feature.isolateShape(e.latlng)
  },
})

U.BaseVertexAction = U.BaseFeatureAction.extend({
  initialize: function (map, feature, latlng, vertex) {
    this.vertex = vertex
    U.BaseFeatureAction.prototype.initialize.call(this, map, feature, latlng)
  },
})

U.DeleteVertexAction = U.BaseVertexAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-delete-vertex',
      tooltip: L._('Delete this vertex (Alt+Click)'),
    },
  },

  onClick: function () {
    this.vertex.delete()
  },
})

U.SplitLineAction = U.BaseVertexAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-split-line',
      tooltip: L._('Split line'),
    },
  },

  onClick: function () {
    this.vertex.split()
  },
})

U.ContinueLineAction = U.BaseVertexAction.extend({
  options: {
    toolbarIcon: {
      className: 'umap-continue-line',
      tooltip: L._('Continue line'),
    },
  },

  onClick: function () {
    this.vertex.continue()
  },
})

// Leaflet.Toolbar doesn't allow twice same toolbar class…
U.SettingsToolbar = L.Toolbar.Control.extend({})
U.DrawToolbar = L.Toolbar.Control.extend({
  initialize: function (options) {
    L.Toolbar.Control.prototype.initialize.call(this, options)
    this.map = this.options.map
    this.map.on('seteditedfeature', this.redraw, this)
  },

  appendToContainer: function (container) {
    this.options.actions = []
    if (this.map.options.enableMarkerDraw) {
      this.options.actions.push(U.DrawMarkerAction)
    }
    if (this.map.options.enablePolylineDraw) {
      this.options.actions.push(U.DrawPolylineAction)
      if (this.map.editedFeature && this.map.editedFeature instanceof U.Polyline) {
        this.options.actions.push(U.AddPolylineShapeAction)
      }
    }
    if (this.map.options.enablePolygonDraw) {
      this.options.actions.push(U.DrawPolygonAction)
      if (this.map.editedFeature && this.map.editedFeature instanceof U.Polygon) {
        this.options.actions.push(U.AddPolygonShapeAction)
      }
    }
    L.Toolbar.Control.prototype.appendToContainer.call(this, container)
  },

  redraw: function () {
    const container = this._control.getContainer()
    container.innerHTML = ''
    this.appendToContainer(container)
  },
})

U.DropControl = L.Class.extend({
  initialize: function (map) {
    this.map = map
    this.dropzone = map._container
  },

  enable: function () {
    L.DomEvent.on(this.dropzone, 'dragenter', this.dragenter, this)
    L.DomEvent.on(this.dropzone, 'dragover', this.dragover, this)
    L.DomEvent.on(this.dropzone, 'drop', this.drop, this)
    L.DomEvent.on(this.dropzone, 'dragleave', this.dragleave, this)
  },

  disable: function () {
    L.DomEvent.off(this.dropzone, 'dragenter', this.dragenter, this)
    L.DomEvent.off(this.dropzone, 'dragover', this.dragover, this)
    L.DomEvent.off(this.dropzone, 'drop', this.drop, this)
    L.DomEvent.off(this.dropzone, 'dragleave', this.dragleave, this)
  },

  dragenter: function (e) {
    L.DomEvent.stop(e)
    this.map.scrollWheelZoom.disable()
    this.dropzone.classList.add('umap-dragover')
  },

  dragover: function (e) {
    L.DomEvent.stop(e)
  },

  drop: function (e) {
    this.map.scrollWheelZoom.enable()
    this.dropzone.classList.remove('umap-dragover')
    L.DomEvent.stop(e)
    for (let i = 0, file; (file = e.dataTransfer.files[i]); i++) {
      this.map.processFileToImport(file)
    }
    this.map.onceDataLoaded(this.map.fitDataBounds)
  },

  dragleave: function () {
    this.map.scrollWheelZoom.enable()
    this.dropzone.classList.remove('umap-dragover')
  },
})

U.EditControl = L.Control.extend({
  options: {
    position: 'topright',
  },

  onAdd: function (map) {
    const container = L.DomUtil.create('div', 'leaflet-control-edit-enable')
    const enableEditing = L.DomUtil.createButton(
      '',
      container,
      L._('Edit'),
      map.enableEdit,
      map
    )
    L.DomEvent.on(
      enableEditing,
      'mouseover',
      function () {
        map.ui.tooltip({
          content: map.help.displayLabel('TOGGLE_EDIT'),
          anchor: enableEditing,
          position: 'bottom',
          delay: 750,
          duration: 5000,
        })
      },
      this
    )

    return container
  },
})

U.MoreControls = L.Control.extend({
  options: {
    position: 'topleft',
  },

  onAdd: function () {
    const container = L.DomUtil.create('div', 'umap-control-text')
    const moreButton = L.DomUtil.createButton(
      'umap-control-more',
      container,
      L._('More controls'),
      this.toggle,
      this
    )
    const lessButton = L.DomUtil.createButton(
      'umap-control-less',
      container,
      L._('Hide controls'),
      this.toggle,
      this
    )
    return container
  },

  toggle: function () {
    const pos = this.getPosition(),
      corner = this._map._controlCorners[pos],
      className = 'umap-more-controls'
    if (L.DomUtil.hasClass(corner, className)) L.DomUtil.removeClass(corner, className)
    else L.DomUtil.addClass(corner, className)
  },
})

U.PermanentCreditsControl = L.Control.extend({
  options: {
    position: 'bottomleft',
  },

  initialize: function (map, options) {
    this.map = map
    L.Control.prototype.initialize.call(this, options)
  },

  onAdd: function () {
    const paragraphContainer = L.DomUtil.create(
        'div',
        'umap-permanent-credits-container'
      ),
      creditsParagraph = L.DomUtil.create('p', '', paragraphContainer)

    this.paragraphContainer = paragraphContainer
    this.setCredits()
    this.setBackground()

    return paragraphContainer
  },

  setCredits: function () {
    this.paragraphContainer.innerHTML = U.Utils.toHTML(this.map.options.permanentCredit)
  },

  setBackground: function () {
    if (this.map.options.permanentCreditBackground) {
      this.paragraphContainer.style.backgroundColor = '#FFFFFFB0'
    } else {
      this.paragraphContainer.style.backgroundColor = ''
    }
  },
})

L.Control.Button = L.Control.extend({
  initialize: function (map, options) {
    this.map = map
    L.Control.prototype.initialize.call(this, options)
  },

  getClassName: function () {
    return this.options.className
  },

  onAdd: function (map) {
    const container = L.DomUtil.create('div', `${this.getClassName()} umap-control`)
    const button = L.DomUtil.createButton(
      '',
      container,
      this.options.title,
      this.onClick,
      this
    )
    L.DomEvent.on(button, 'dblclick', L.DomEvent.stopPropagation)
    this.afterAdd(container)
    return container
  },

  afterAdd: function (container) {},
})

U.DataLayersControl = L.Control.Button.extend({
  options: {
    position: 'topleft',
    className: 'umap-control-browse',
    title: L._('See layers'),
  },

  afterAdd: function (container) {
    U.Utils.toggleBadge(container, this.map.browser.hasFilters())
  },

  onClick: function () {
    this.map.openBrowser()
  },
})

U.CaptionControl = L.Control.Button.extend({
  options: {
    position: 'topleft',
    className: 'umap-control-caption',
    title: L._('About'),
  },

  onClick: function () {
    this.map.openCaption()
  },
})

U.StarControl = L.Control.Button.extend({
  options: {
    position: 'topleft',
    title: L._('Star this map'),
  },

  getClassName: function () {
    const status = this.map.options.starred ? ' starred' : ''
    return `leaflet-control-star umap-control${status}`
  },

  onClick: function () {
    this.map.star()
  },
})

L.Control.Embed = L.Control.Button.extend({
  options: {
    position: 'topleft',
    title: L._('Share and download'),
    className: 'leaflet-control-embed umap-control',
  },

  onClick: function () {
    this.map.share.open()
  },
})

U.DataLayer.include({
  renderLegend: function (container) {
    if (this.layer.renderLegend) return this.layer.renderLegend(container)
    const color = L.DomUtil.create('span', 'datalayer-color', container)
    color.style.backgroundColor = this.getColor()
  },

  renderToolbox: function (container) {
    const toggle = L.DomUtil.createButtonIcon(
      container,
      'icon-eye',
      L._('Show/hide layer')
    )
    const zoomTo = L.DomUtil.createButtonIcon(
      container,
      'icon-zoom',
      L._('Zoom to layer extent')
    )
    const edit = L.DomUtil.createButtonIcon(
      container,
      'icon-edit show-on-edit',
      L._('Edit')
    )
    const table = L.DomUtil.createButtonIcon(
      container,
      'icon-table show-on-edit',
      L._('Edit properties in a table')
    )
    const remove = L.DomUtil.createButtonIcon(
      container,
      'icon-delete show-on-edit',
      L._('Delete layer')
    )
    if (this.isReadOnly()) {
      L.DomUtil.addClass(container, 'readonly')
    } else {
      L.DomEvent.on(edit, 'click', this.edit, this)
      L.DomEvent.on(table, 'click', this.tableEdit, this)
      L.DomEvent.on(
        remove,
        'click',
        function () {
          if (!this.isVisible()) return
          if (!confirm(L._('Are you sure you want to delete this layer?'))) return
          this._delete()
        },
        this
      )
    }
    L.DomEvent.on(toggle, 'click', this.toggle, this)
    L.DomEvent.on(zoomTo, 'click', this.zoomTo, this)
    container.classList.add(this.getHidableClass())
    container.classList.toggle('off', !this.isVisible())
  },

  getHidableElements: function () {
    return document.querySelectorAll(`.${this.getHidableClass()}`)
  },

  getHidableClass: function () {
    return `show_with_datalayer_${L.stamp(this)}`
  },

  propagateDelete: function () {
    const els = this.getHidableElements()
    for (const el of els) {
      L.DomUtil.remove(el)
    }
  },

  propagateRemote: function () {
    const els = this.getHidableElements()
    for (const el of els) {
      el.classList.toggle('remotelayer', this.isRemoteLayer())
    }
  },

  propagateHide: function () {
    const els = this.getHidableElements()
    for (let i = 0; i < els.length; i++) {
      L.DomUtil.addClass(els[i], 'off')
    }
  },

  propagateShow: function () {
    this.onceLoaded(function () {
      const els = this.getHidableElements()
      for (let i = 0; i < els.length; i++) {
        L.DomUtil.removeClass(els[i], 'off')
      }
    }, this)
  },
})

U.DataLayer.addInitHook(function () {
  this.on('hide', this.propagateHide)
  this.on('show', this.propagateShow)
  this.on('erase', this.propagateDelete)
  if (this.isVisible()) this.propagateShow()
})

const ControlsMixin = {
  HIDDABLE_CONTROLS: [
    'zoom',
    'search',
    'fullscreen',
    'embed',
    'datalayers',
    'caption',
    'locate',
    'measure',
    'editinosm',
    'star',
    'tilelayers',
  ],

  renderEditToolbar: function () {
    const container = L.DomUtil.create(
      'div',
      'umap-main-edit-toolbox with-transition dark',
      this._controlContainer
    )
    const leftContainer = L.DomUtil.create('div', 'umap-left-edit-toolbox', container)
    const rightContainer = L.DomUtil.create('div', 'umap-right-edit-toolbox', container)
    const logo = L.DomUtil.create('div', 'logo', leftContainer)
    L.DomUtil.createLink('', logo, 'uMap', '/', null, L._('Go to the homepage'))
    const nameButton = L.DomUtil.createButton('map-name', leftContainer, '')
    L.DomEvent.on(
      nameButton,
      'mouseover',
      function () {
        this.ui.tooltip({
          content: L._('Edit the title of the map'),
          anchor: nameButton,
          position: 'bottom',
          delay: 500,
          duration: 5000,
        })
      },
      this
    )
    const shareStatusButton = L.DomUtil.createButton(
      'share-status',
      leftContainer,
      '',
      this.permissions.edit,
      this.permissions
    )
    L.DomEvent.on(
      shareStatusButton,
      'mouseover',
      function () {
        this.ui.tooltip({
          content: L._('Update who can see and edit the map'),
          anchor: shareStatusButton,
          position: 'bottom',
          delay: 500,
          duration: 5000,
        })
      },
      this
    )
    const update = () => {
      const status = this.permissions.getShareStatusDisplay()
      nameButton.textContent = this.getDisplayName()
      // status is not set until map is saved once
      if (status) {
        shareStatusButton.textContent = L._('Visibility: {status}', {
          status: status,
        })
      }
    }
    update()
    this.once('saved', L.bind(update, this))
    if (this.options.editMode === 'advanced') {
      L.DomEvent.on(nameButton, 'click', this.editCaption, this)
      L.DomEvent.on(shareStatusButton, 'click', this.permissions.edit, this.permissions)
    }
    this.on('postsync', L.bind(update, this))
    if (this.options.user) {
      L.DomUtil.createLink(
        'umap-user',
        rightContainer,
        L._(`My Dashboard ({username})`, {
          username: this.options.user.name,
        }),
        this.options.user.url
      )
    }
    this.help.link(rightContainer, 'edit')
    const controlEditCancel = L.DomUtil.createButton(
      'leaflet-control-edit-cancel',
      rightContainer,
      L.DomUtil.add('span', '', null, L._('Cancel edits')),
      this.askForReset,
      this
    )
    L.DomEvent.on(
      controlEditCancel,
      'mouseover',
      function () {
        this.ui.tooltip({
          content: this.help.displayLabel('CANCEL'),
          anchor: controlEditCancel,
          position: 'bottom',
          delay: 500,
          duration: 5000,
        })
      },
      this
    )
    const controlEditDisable = L.DomUtil.createButton(
      'leaflet-control-edit-disable',
      rightContainer,
      L.DomUtil.add('span', '', null, L._('View')),
      this.disableEdit,
      this
    )
    L.DomEvent.on(
      controlEditDisable,
      'mouseover',
      function () {
        this.ui.tooltip({
          content: this.help.displayLabel('PREVIEW'),
          anchor: controlEditDisable,
          position: 'bottom',
          delay: 500,
          duration: 5000,
        })
      },
      this
    )
    const controlEditSave = L.DomUtil.createButton(
      'leaflet-control-edit-save button',
      rightContainer,
      L.DomUtil.add('span', '', null, L._('Save')),
      this.save,
      this
    )
    L.DomEvent.on(
      controlEditSave,
      'mouseover',
      function () {
        this.ui.tooltip({
          content: this.help.displayLabel('SAVE'),
          anchor: controlEditSave,
          position: 'bottom',
          delay: 500,
          duration: 5000,
        })
      },
      this
    )
  },

  editDatalayers: function () {
    if (!this.editEnabled) return
    const container = L.DomUtil.create('div')
    L.DomUtil.createTitle(container, L._('Manage layers'), 'icon-layers')
    const ul = L.DomUtil.create('ul', '', container)
    this.eachDataLayerReverse((datalayer) => {
      const row = L.DomUtil.create('li', 'orderable', ul)
      L.DomUtil.createIcon(row, 'icon-drag', L._('Drag to reorder'))
      datalayer.renderToolbox(row)
      const title = L.DomUtil.add('span', '', row, datalayer.options.name)
      row.classList.toggle('off', !datalayer.isVisible())
      title.textContent = datalayer.options.name
      row.dataset.id = L.stamp(datalayer)
    })
    const onReorder = (src, dst, initialIndex, finalIndex) => {
      const layer = this.datalayers[src.dataset.id],
        other = this.datalayers[dst.dataset.id],
        minIndex = Math.min(layer.getRank(), other.getRank()),
        maxIndex = Math.max(layer.getRank(), other.getRank())
      if (finalIndex === 0) layer.bringToTop()
      else if (finalIndex > initialIndex) layer.insertBefore(other)
      else layer.insertAfter(other)
      this.eachDataLayerReverse((datalayer) => {
        if (datalayer.getRank() >= minIndex && datalayer.getRank() <= maxIndex)
          datalayer.isDirty = true
      })
      this.indexDatalayers()
    }
    const orderable = new U.Orderable(ul, onReorder)

    const bar = L.DomUtil.create('div', 'button-bar', container)
    L.DomUtil.createButton(
      'show-on-edit block add-datalayer button',
      bar,
      L._('Add a layer'),
      this.newDataLayer,
      this
    )

    this.editPanel.open({ content: container })
  },
}

/* Used in view mode to define the current tilelayer */
U.TileLayerControl = L.Control.IconLayers.extend({
  initialize: function (map, options) {
    this.map = map
    L.Control.IconLayers.prototype.initialize.call(this, {
      position: 'topleft',
      manageLayers: false,
    })
    this.on('activelayerchange', (e) => map.selectTileLayer(e.layer))
  },

  setLayers: function (layers) {
    if (!layers) {
      layers = []
      this.map.eachTileLayer((layer) => {
        try {
          // We'd like to use layer.getTileUrl, but this method will only work
          // when the tilelayer is actually added to the map (needs this._tileZoom
          // to be defined)
          // Fixme when https://github.com/Leaflet/Leaflet/pull/9201 is released
          const icon = U.Utils.template(
            layer.options.url_template,
            this.map.demoTileInfos
          )
          layers.push({
            title: layer.options.name,
            layer: layer,
            icon: icon,
          })
        } catch (e) {
          // Skip this tilelayer
          console.error(e)
        }
      })
    }
    const maxShown = 10
    L.Control.IconLayers.prototype.setLayers.call(this, layers.slice(0, maxShown))
    if (this.map.selected_tilelayer) this.setActiveLayer(this.map.selected_tilelayer)
  },
})

/* Used in edit mode to define the default tilelayer */
U.TileLayerChooser = L.Control.extend({
  options: {
    position: 'topleft',
  },

  initialize: function (map, options) {
    this.map = map
    L.Control.prototype.initialize.call(this, options)
  },

  onAdd: function () {
    const container = L.DomUtil.create('div', 'leaflet-control-tilelayers umap-control')
    const changeMapBackgroundButton = L.DomUtil.createButton(
      '',
      container,
      L._('Change map background'),
      this.openSwitcher,
      this
    )
    L.DomEvent.on(changeMapBackgroundButton, 'dblclick', L.DomEvent.stopPropagation)
    return container
  },

  openSwitcher: function (options) {
    const container = L.DomUtil.create('div', 'umap-tilelayer-switcher-container')
    L.DomUtil.createTitle(container, L._('Change tilelayers'), 'icon-tilelayer')
    this._tilelayers_container = L.DomUtil.create('ul', '', container)
    this.buildList(options)
    this.map.editPanel.open({
      content: container,
      className: options.className,
    })
  },

  buildList: function (options) {
    this.map.eachTileLayer(function (tilelayer) {
      if (
        window.location.protocol === 'https:' &&
        tilelayer.options.url_template.indexOf('http:') === 0
      )
        return
      this.addTileLayerElement(tilelayer, options)
    }, this)
  },

  addTileLayerElement: function (tilelayer, options) {
    const selectedClass = this.map.hasLayer(tilelayer) ? 'selected' : '',
      el = L.DomUtil.create('li', selectedClass, this._tilelayers_container),
      img = L.DomUtil.create('img', '', el),
      name = L.DomUtil.create('div', '', el)
    img.src = U.Utils.template(tilelayer.options.url_template, this.map.demoTileInfos)
    img.loading = 'lazy'
    name.textContent = tilelayer.options.name
    L.DomEvent.on(
      el,
      'click',
      function () {
        this.map.selectTileLayer(tilelayer)
        this.map._controls.tilelayers.setLayers()
        if (options && options.callback) options.callback(tilelayer)
      },
      this
    )
  },
})

U.AttributionControl = L.Control.Attribution.extend({
  options: {
    prefix: '',
  },

  _update: function () {
    // Layer is no more on the map
    if (!this._map) return
    L.Control.Attribution.prototype._update.call(this)
    // Use our own container, so we can hide/show on small screens
    const credits = this._container.innerHTML
    this._container.innerHTML = ''
    const container = L.DomUtil.create('div', 'attribution-container', this._container)
    container.innerHTML = credits
    const shortCredit = this._map.getOption('shortCredit'),
      captionMenus = this._map.getOption('captionMenus')
    if (shortCredit) {
      L.DomUtil.element({
        tagName: 'span',
        parent: container,
        safeHTML: ` — ${U.Utils.toHTML(shortCredit)}`,
      })
    }
    if (captionMenus) {
      const link = L.DomUtil.add('a', '', container, ` — ${L._('About')}`)
      L.DomEvent.on(link, 'click', L.DomEvent.stop)
        .on(link, 'click', this._map.openCaption, this._map)
        .on(link, 'dblclick', L.DomEvent.stop)
    }
    if (window.top === window.self && captionMenus) {
      // We are not in iframe mode
      L.DomUtil.createLink('', container, ` — ${L._('Home')}`, '/')
    }
    if (captionMenus) {
      L.DomUtil.createLink(
        '',
        container,
        ` — ${L._('Powered by uMap')}`,
        'https://umap-project.org/'
      )
    }
    L.DomUtil.createLink('attribution-toggle', this._container, '')
  },
})

/*
 * Take control over L.Control.Locate to be able to
 * call start() before adding the control (and thus the button) to the map.
 */
U.Locate = L.Control.Locate.extend({
  initialize: function (map, options) {
    // When calling start(), it will try to add a location marker
    // on the layer, which is normally added in the addTo/onAdd method
    this._layer = this.options.layer = new L.LayerGroup()
    // When calling start(), it will call _activate(), which then adds
    // location related event listeners on the map
    this.map = map
    L.Control.Locate.prototype.initialize.call(this, options)
  },

  onAdd: function (map) {
    const active = this._active
    const container = L.Control.Locate.prototype.onAdd.call(this, map)
    this._active = active
    return container
  },

  _activate: function () {
    this._map = this.map
    L.Control.Locate.prototype._activate.call(this)
  },

  remove: function () {
    // Prevent to call remove if the control is not really added to the map
    // This occurs because we do create the control and call its activate
    // method before adding the control button itself to the map, in the
    // case where the map defaultView is set to "location"
    if (!this._container || !this._container.parentNode) return
    return L.Control.Locate.prototype.remove.call(this)
  },

})

U.Search = L.PhotonSearch.extend({
  initialize: function (map, input, options) {
    this.options.placeholder = L._('Type a place name or coordinates')
    this.options.location_bias_scale = 0.5
    L.PhotonSearch.prototype.initialize.call(this, map, input, options)
    this.options.url = map.options.urls.search
    if (map.options.maxBounds) this.options.bbox = map.options.maxBounds.toBBoxString()
    this.reverse = new L.PhotonReverse({
      handleResults: (geojson) => {
        this.handleResultsWithReverse(geojson)
      },
    })
  },

  handleResultsWithReverse: function (geojson) {
    const latlng = this.reverse.latlng
    geojson.features.unshift({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [latlng.lng, latlng.lat] },
      properties: {
        name: L._('Go to "{coords}"', { coords: `${latlng.lat} ${latlng.lng}` }),
      },
    })

    this.handleResults(geojson)
  },

  search: function () {
    const pattern = /^(?<lat>[-+]?\d{1,2}[.,]\d+)\s*[ ,]\s*(?<lng>[-+]?\d{1,3}[.,]\d+)$/
    if (pattern.test(this.input.value)) {
      this.hide()
      const { lat, lng } = pattern.exec(this.input.value).groups
      const latlng = L.latLng(lat, lng)
      if (latlng.isValid()) {
        this.reverse.doReverse(latlng)
      } else {
        this.map.ui.alert({ content: 'Invalid latitude or longitude', mode: 'error' })
      }
      return
    }
    // Only numbers, abort.
    if (/^[\d .,]*$/.test(this.input.value)) return
    // Do normal search
    this.options.includePosition = this.map.getZoom() > 10
    L.PhotonSearch.prototype.search.call(this)
  },

  onBlur: function (e) {
    // Overrided because we don't want to hide the results on blur.
    this.fire('blur')
  },

  formatResult: function (feature, el) {
    const tools = L.DomUtil.create('span', 'search-result-tools', el)
    const zoom = L.DomUtil.createButtonIcon(
      tools,
      'icon-zoom',
      L._('Zoom to this place')
    )
    const edit = L.DomUtil.createButtonIcon(
      tools,
      'icon-edit',
      L._('Save this location as new feature')
    )
    // We need to use "mousedown" because Leaflet.Photon listen to mousedown
    // on el.
    L.DomEvent.on(zoom, 'mousedown', (e) => {
      L.DomEvent.stop(e)
      this.zoomToFeature(feature)
    })
    L.DomEvent.on(edit, 'mousedown', (e) => {
      L.DomEvent.stop(e)
      const datalayer = this.map.defaultEditDataLayer()
      const layer = datalayer.geojsonToFeatures(feature)
      layer.isDirty = true
      layer.edit()
    })
    this._formatResult(feature, el)
  },

  zoomToFeature: function (feature) {
    const zoom = Math.max(this.map.getZoom(), 16) // Never unzoom.
    this.map.setView(
      [feature.geometry.coordinates[1], feature.geometry.coordinates[0]],
      zoom
    )
  },

  onSelected: function (feature) {
    this.zoomToFeature(feature)
    this.map.panel.close()
  },
})

U.SearchControl = L.Control.extend({
  options: {
    position: 'topleft',
  },

  onAdd: function (map) {
    this.map = map
    const container = L.DomUtil.create('div', 'leaflet-control-search umap-control')
    L.DomEvent.disableClickPropagation(container)
    L.DomUtil.createButton(
      '',
      container,
      L._('Search location'),
      (e) => {
        L.DomEvent.stop(e)
        this.open()
      },
      this
    )
    return container
  },

  open: function () {
    const options = {
      limit: 10,
      noResultLabel: L._('No results'),
    }
    if (this.map.options.photonUrl) options.url = this.map.options.photonUrl
    const container = L.DomUtil.create('div', '')

    L.DomUtil.createTitle(container, L._('Search location'), 'icon-search')
    const input = L.DomUtil.create('input', 'photon-input', container)
    const resultsContainer = L.DomUtil.create('div', 'photon-autocomplete', container)
    this.search = new U.Search(this.map, input, options)
    const id = Math.random()
    this.search.on('ajax:send', () => {
      this.map.fire('dataloading', { id: id })
    })
    this.search.on('ajax:return', () => {
      this.map.fire('dataload', { id: id })
    })
    this.search.resultsContainer = resultsContainer
    this.map.panel.open({ content: container }).then(input.focus())
  },
})

L.Control.MiniMap.include({
  initialize: function (layer, options) {
    L.Util.setOptions(this, options)
    this._layer = this._cloneLayer(layer)
  },

  onMainMapBaseLayerChange: function (e) {
    const layer = this._cloneLayer(e.layer)
    if (this._miniMap.hasLayer(this._layer)) {
      this._miniMap.removeLayer(this._layer)
    }
    this._layer = layer
    this._miniMap.addLayer(this._layer)
  },

  _cloneLayer: function (layer) {
    return new L.TileLayer(layer._url, L.Util.extend({}, layer.options))
  },
})

L.Control.Loading.include({
  onAdd: function (map) {
    this._container = L.DomUtil.create('div', 'umap-loader', map._controlContainer)
    map.on('baselayerchange', this._layerAdd, this)
    this._addMapListeners(map)
    this._map = map
  },

  _showIndicator: function () {
    L.DomUtil.addClass(this._map._container, 'umap-loading')
  },

  _hideIndicator: function () {
    L.DomUtil.removeClass(this._map._container, 'umap-loading')
  },
})

/*
 * Make it dynamic
 */
U.ContextMenu = L.Map.ContextMenu.extend({
  _createItems: function (e) {
    this._map.setContextMenuItems(e)
    L.Map.ContextMenu.prototype._createItems.call(this)
  },

  _showAtPoint: function (pt, e) {
    this._items = []
    this._container.innerHTML = ''
    this._createItems(e)
    L.Map.ContextMenu.prototype._showAtPoint.call(this, pt, e)
  },
})

U.Editable = L.Editable.extend({
  initialize: function (map, options) {
    L.Editable.prototype.initialize.call(this, map, options)
    this.on('editable:drawing:click editable:drawing:move', this.drawingTooltip)
    this.on('editable:drawing:end', (e) => {
      this.closeTooltip()
      // Leaflet.Editable will delete the drawn shape if invalid
      // (eg. line has only one drawn point)
      // So let's check if the layer has no more shape
      if (!e.layer.hasGeom()) e.layer.del()
      else e.layer.edit()
    })
    // Layer for items added by users
    this.on('editable:drawing:cancel', (e) => {
      if (e.layer instanceof U.Marker) e.layer.del()
    })
    this.on('editable:drawing:commit', function (e) {
      e.layer.isDirty = true
      if (this.map.editedFeature !== e.layer) e.layer.edit(e)
    })
    this.on('editable:editing', (e) => {
      const layer = e.layer
      layer.isDirty = true
      if (layer._tooltip && layer.isTooltipOpen()) {
        layer._tooltip.setLatLng(layer.getCenter())
        layer._tooltip.update()
      }
    })
    this.on('editable:vertex:ctrlclick', (e) => {
      const index = e.vertex.getIndex()
      if (index === 0 || (index === e.vertex.getLastIndex() && e.vertex.continue))
        e.vertex.continue()
    })
    this.on('editable:vertex:altclick', (e) => {
      if (e.vertex.editor.vertexCanBeDeleted(e.vertex)) e.vertex.delete()
    })
    this.on('editable:vertex:rawclick', this.onVertexRawClick)
  },

  createPolyline: function (latlngs) {
    return new U.Polyline(this.map, latlngs, this._getDefaultProperties())
  },

  createPolygon: function (latlngs) {
    return new U.Polygon(this.map, latlngs, this._getDefaultProperties())
  },

  createMarker: function (latlng) {
    return new U.Marker(this.map, latlng, this._getDefaultProperties())
  },

  _getDefaultProperties: function () {
    const result = {}
    if (this.map.options.featuresHaveOwner && this.map.options.hasOwnProperty('user')) {
      result.geojson = { properties: { owner: this.map.options.user.id } }
    }
    return result
  },

  connectCreatedToMap: function (layer) {
    // Overrided from Leaflet.Editable
    const datalayer = this.map.defaultEditDataLayer()
    datalayer.addLayer(layer)
    layer.isDirty = true
    return layer
  },

  drawingTooltip: function (e) {
    if (e.layer instanceof L.Marker && e.type == 'editable:drawing:start') {
      this.map.ui.tooltip({ content: L._('Click to add a marker') })
    }
    if (!(e.layer instanceof L.Polyline)) {
      // only continue with Polylines and Polygons
      return
    }

    let content = L._('Drawing')
    let measure
    if (e.layer.editor._drawnLatLngs) {
      // when drawing (a Polyline or Polygon)
      if (!e.layer.editor._drawnLatLngs.length) {
        // when drawing first point
        if (e.layer instanceof L.Polygon) {
          content = L._('Click to start drawing a polygon')
        } else if (e.layer instanceof L.Polyline) {
          content = L._('Click to start drawing a line')
        }
      } else {
        const tmpLatLngs = e.layer.editor._drawnLatLngs.slice()
        tmpLatLngs.push(e.latlng)
        measure = e.layer.getMeasure(tmpLatLngs)

        if (e.layer.editor._drawnLatLngs.length < e.layer.editor.MIN_VERTEX) {
          // when drawing second point
          content = L._('Click to continue drawing')
        } else {
          // when drawing third point (or more)
          content = L._('Click last point to finish shape')
        }
      }
    } else {
      // when moving an existing point
      measure = e.layer.getMeasure()
    }
    if (measure) {
      if (e.layer instanceof L.Polygon) {
        content += L._(' (area: {measure})', { measure: measure })
      } else if (e.layer instanceof L.Polyline) {
        content += L._(' (length: {measure})', { measure: measure })
      }
    }
    if (content) {
      this.map.ui.tooltip({ content: content })
    }
  },

  closeTooltip: function () {
    this.map.ui.closeTooltip()
  },

  onVertexRawClick: function (e) {
    e.layer.onVertexRawClick(e)
    L.DomEvent.stop(e)
    e.cancel()
  },
})
