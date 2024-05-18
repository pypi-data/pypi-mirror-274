L.Map.mergeOptions({
  overlay: null,
  datalayers: [],
  hash: true,
  maxZoomLimit: 24,
  attributionControl: false,
  editMode: 'advanced',
  noControl: false, // Do not render any control.
  name: '',
  description: '',
  // When a TileLayer is in TMS mode, it needs -y instead of y.
  // This is usually handled by the TileLayer instance itself, but
  // we cannot rely on this because of the y is overriden by Leaflet
  // See https://github.com/Leaflet/Leaflet/pull/9201
  // And let's remove this -y when this PR is merged and released.
  demoTileInfos: { 's': 'a', 'z': 9, 'x': 265, 'y': 181, '-y': 181, 'r': '' },
  licences: [],
  licence: '',
  enableMarkerDraw: true,
  enablePolygonDraw: true,
  enablePolylineDraw: true,
  limitBounds: {},
  importPresets: [
    // {url: 'http://localhost:8019/en/datalayer/1502/', label: 'Simplified World Countries', format: 'geojson'}
  ],
  slideshow: {},
  clickable: true,
  permissions: {},
  featuresHaveOwner: false,
})

U.Map = L.Map.extend({
  includes: [ControlsMixin],

  initialize: function (el, geojson) {
    // Locale name (pt_PT, en_US…)
    // To be used for Django localization
    if (geojson.properties.locale) L.setLocale(geojson.properties.locale)

    // Language code (pt-pt, en-us…)
    // To be used in javascript APIs
    if (geojson.properties.lang) L.lang = geojson.properties.lang

    this.setOptionsFromQueryString(geojson.properties)
    // Prevent default creation of controls
    const zoomControl = geojson.properties.zoomControl
    const fullscreenControl = geojson.properties.fullscreenControl
    geojson.properties.zoomControl = false
    geojson.properties.fullscreenControl = false

    L.Map.prototype.initialize.call(this, el, geojson.properties)

    if (geojson.properties.schema) this.overrideSchema(geojson.properties.schema)

    // After calling parent initialize, as we are doing initCenter our-selves
    if (geojson.geometry) this.options.center = this.latLng(geojson.geometry)
    this.urls = new U.URLs(this.options.urls)

    this.panel = new U.Panel(this)
    if (this.hasEditMode()) {
      this.editPanel = new U.EditPanel(this)
      this.fullPanel = new U.FullPanel(this)
    }
    this.ui = new U.UI(this._container)
    this.ui.on('dataloading', (e) => this.fire('dataloading', e))
    this.ui.on('dataload', (e) => this.fire('dataload', e))
    this.server = new U.ServerRequest(this.ui)
    this.request = new U.Request(this.ui)

    this.initLoader()
    this.name = this.options.name
    this.description = this.options.description
    this.demoTileInfos = this.options.demoTileInfos
    this.options.zoomControl = zoomControl !== undefined ? zoomControl : true
    this.options.fullscreenControl =
      fullscreenControl !== undefined ? fullscreenControl : true

    this.datalayersFromQueryString = L.Util.queryString('datalayers')
    if (this.datalayersFromQueryString) {
      this.datalayersFromQueryString = this.datalayersFromQueryString
        .toString()
        .split(',')
    }

    let editedFeature = null
    const self = this
    try {
      Object.defineProperty(this, 'editedFeature', {
        get: function () {
          return editedFeature
        },
        set: function (feature) {
          if (editedFeature && editedFeature !== feature) {
            editedFeature.endEdit()
          }
          editedFeature = feature
          self.fire('seteditedfeature')
        },
      })
    } catch (e) {
      // Certainly IE8, which has a limited version of defineProperty
    }

    // Retrocompat
    if (
      this.options.slideshow &&
      this.options.slideshow.delay &&
      this.options.slideshow.active === undefined
    ) {
      this.options.slideshow.active = true
    }
    if (this.options.advancedFilterKey) {
      this.options.facetKey = this.options.advancedFilterKey
      delete this.options.advancedFilterKey
    }

    // Global storage for retrieving datalayers and features
    this.datalayers = {}
    this.datalayers_index = []
    this.dirty_datalayers = []
    this.features_index = {}

    // Needed for actions labels
    this.help = new U.Help(this)

    this.initControls()
    // Needs locate control and hash to exist
    this.initCenter()
    this.initTileLayers()
    // Needs tilelayer to exist for minimap
    this.renderControls()
    this.handleLimitBounds()
    this.initDataLayers()

    if (this.options.displayCaptionOnLoad) {
      // Retrocompat
      if (!this.options.onLoadPanel) {
        this.options.onLoadPanel = 'caption'
      }
      delete this.options.displayCaptionOnLoad
    }
    if (this.options.displayDataBrowserOnLoad) {
      // Retrocompat
      if (!this.options.onLoadPanel) {
        this.options.onLoadPanel = 'databrowser'
      }
      delete this.options.displayDataBrowserOnLoad
    }
    if (this.options.datalayersControl === 'expanded') {
      this.options.onLoadPanel = 'datalayers'
    }
    if (this.options.onLoadPanel === 'facet') {
      this.options.onLoadPanel = 'datafilters'
    }

    let isDirty = false // self status
    try {
      Object.defineProperty(this, 'isDirty', {
        get: function () {
          return isDirty
        },
        set: function (status) {
          isDirty = status
          this.checkDirty()
        },
      })
    } catch (e) {
      // Certainly IE8, which has a limited version of defineProperty
    }
    this.on(
      'baselayerchange',
      function (e) {
        if (this._controls.miniMap) this._controls.miniMap.onMainMapBaseLayerChange(e)
      },
      this
    )

    // Creation mode
    if (!this.options.umap_id) {
      if (!this.options.preview) {
        this.isDirty = true
        this.enableEdit()
      }
      this._default_extent = true
      this.options.name = L._('Untitled map')
      let data = L.Util.queryString('data', null)
      let dataUrl = L.Util.queryString('dataUrl', null)
      const dataFormat = L.Util.queryString('dataFormat', 'geojson')
      if (dataUrl) {
        dataUrl = decodeURIComponent(dataUrl)
        dataUrl = this.localizeUrl(dataUrl)
        dataUrl = this.proxyUrl(dataUrl)
        const datalayer = this.createDataLayer()
        datalayer.importFromUrl(dataUrl, dataFormat)
      } else if (data) {
        data = decodeURIComponent(data)
        const datalayer = this.createDataLayer()
        datalayer.importRaw(data, dataFormat)
      }
    }

    this.slideshow = new U.Slideshow(this, this.options.slideshow)
    this.permissions = new U.MapPermissions(this)
    if (this.hasEditMode()) {
      this.editTools = new U.Editable(this)
      this.renderEditToolbar()
    }
    this.initShortcuts()
    this.onceDataLoaded(function () {
      const slug = L.Util.queryString('feature')
      if (slug && this.features_index[slug]) this.features_index[slug].view()
      if (this.options.noControl) return
      this.initCaptionBar()
      if (L.Util.queryString('share')) {
        this.share.open()
      } else if (this.options.onLoadPanel === 'databrowser') {
        this.panel.setDefaultMode('expanded')
        this.openBrowser('data')
      } else if (this.options.onLoadPanel === 'datalayers') {
        this.panel.setDefaultMode('condensed')
        this.openBrowser('layers')
      } else if (this.options.onLoadPanel === 'datafilters') {
        this.panel.setDefaultMode('expanded')
        this.openBrowser('filters')
      } else if (this.options.onLoadPanel === 'caption') {
        this.panel.setDefaultMode('condensed')
        this.openCaption()
      }
      if (L.Util.queryString('edit')) {
        if (this.hasEditMode()) this.enableEdit()
        // Sometimes users share the ?edit link by mistake, let's remove
        // this search parameter from URL to prevent this
        const url = new URL(window.location)
        url.searchParams.delete('edit')
        history.pushState({}, '', url)
      }
      if (L.Util.queryString('download')) {
        const download_url = this.urls.get('map_download', {
          map_id: this.options.umap_id,
        })
        window.location = download_url
      }
    })

    window.onbeforeunload = () => (this.editEnabled && this.isDirty) || null
    this.backup()
    this.initContextMenu()
    this.on('click contextmenu.show', this.closeInplaceToolbar)
  },

  render: function (fields) {
    let impacts = U.Utils.getImpactsFromSchema(fields)

    for (let impact of impacts) {
      switch (impact) {
        case 'ui':
          this.initCaptionBar()
          this.renderEditToolbar()
          this.renderControls()
          this.browser.redraw()
          break
        case 'data':
          this.redrawVisibleDataLayers()
          break
        case 'datalayer-index':
          this.reindexDataLayers()
          break
        case 'background':
          this.initTileLayers()
          break
        case 'bounds':
          this.handleLimitBounds()
          break
      }
    }
  },

  reindexDataLayers: function () {
    this.eachDataLayer((datalayer) => datalayer.reindex())
    this.onDataLayersChanged()
  },

  redrawVisibleDataLayers: function () {
    this.eachVisibleDataLayer((datalayer) => {
      datalayer.redraw()
    })
  },

  setOptionsFromQueryString: function (options) {
    // This is not an editable option
    L.Util.setFromQueryString(options, 'editMode')
    // FIXME retrocompat
    L.Util.setBooleanFromQueryString(options, 'displayDataBrowserOnLoad')
    L.Util.setBooleanFromQueryString(options, 'displayCaptionOnLoad')
    for (const [key, schema] of Object.entries(U.SCHEMA)) {
      switch (schema.type) {
        case Boolean:
          if (schema.nullable) L.Util.setNullableBooleanFromQueryString(options, key)
          else L.Util.setBooleanFromQueryString(options, key)
          break
        case Number:
          L.Util.setNumberFromQueryString(options, key)
          break
        case String:
          L.Util.setFromQueryString(options, key)
          break
      }
    }
    // Specific case for datalayersControl
    // which accepts "expanded" value, on top of true/false/null
    if (L.Util.queryString('datalayersControl') === 'expanded') {
      options.onLoadPanel = 'datalayers'
    }
  },

  // Merge the given schema with the default one
  // Missing keys inside the schema are merged with the default ones.
  overrideSchema: function (schema) {
    for (const [key, extra] of Object.entries(schema)) {
      U.SCHEMA[key] = L.extend({}, U.SCHEMA[key], extra)
    }
  },

  initControls: function () {
    this.helpMenuActions = {}
    this._controls = {}

    if (this.hasEditMode() && !this.options.noControl) {
      new U.EditControl(this).addTo(this)

      new U.DrawToolbar({ map: this }).addTo(this)
      const editActions = [
        U.EditCaptionAction,
        U.EditPropertiesAction,
        U.EditLayersAction,
        U.ChangeTileLayerAction,
        U.UpdateExtentAction,
        U.UpdatePermsAction,
        U.ImportAction,
      ]
      if (this.options.editMode === 'advanced') {
        new U.SettingsToolbar({ actions: editActions }).addTo(this)
      }
    }
    this._controls.zoom = new L.Control.Zoom({
      zoomInTitle: L._('Zoom in'),
      zoomOutTitle: L._('Zoom out'),
    })
    this._controls.datalayers = new U.DataLayersControl(this)
    this._controls.caption = new U.CaptionControl(this)
    this._controls.locate = new U.Locate(this, {
      strings: {
        title: L._('Center map on your location'),
      },
      showPopup: false,
      // We style this control in our own CSS for consistency with other controls,
      // but the control breaks if we don't specify a class here, so a fake class
      // will do.
      icon: 'umap-fake-class',
      iconLoading: 'umap-fake-class',
      flyTo: this.options.easing,
      onLocationError: (err) => this.ui.alert({ content: err.message }),
    })
    this._controls.fullscreen = new L.Control.Fullscreen({
      title: { false: L._('View Fullscreen'), true: L._('Exit Fullscreen') },
    })
    this._controls.search = new U.SearchControl()
    this._controls.embed = new L.Control.Embed(this)
    this._controls.tilelayersChooser = new U.TileLayerChooser(this)
    if (this.options.user) this._controls.star = new U.StarControl(this)
    this._controls.editinosm = new L.Control.EditInOSM({
      position: 'topleft',
      widgetOptions: {
        helpText: L._(
          'Open this map extent in a map editor to provide more accurate data to OpenStreetMap'
        ),
      },
    })
    this._controls.measure = new L.MeasureControl().initHandler(this)
    this._controls.more = new U.MoreControls()
    this._controls.scale = L.control.scale()
    this._controls.permanentCredit = new U.PermanentCreditsControl(this)
    if (this.options.scrollWheelZoom) this.scrollWheelZoom.enable()
    else this.scrollWheelZoom.disable()
    this.browser = new U.Browser(this)
    this.facets = new U.Facets(this)
    this.caption = new U.Caption(this)
    this.importer = new U.Importer(this)
    this.drop = new U.DropControl(this)
    this.share = new U.Share(this)
    this._controls.tilelayers = new U.TileLayerControl(this)
  },

  renderControls: function () {
    const hasSlideshow = Boolean(this.options.slideshow && this.options.slideshow.active)
    const barEnabled = this.options.captionBar || hasSlideshow
    document.body.classList.toggle('umap-caption-bar-enabled', barEnabled)
    document.body.classList.toggle('umap-slideshow-enabled', hasSlideshow)
    for (const control of Object.values(this._controls)) {
      this.removeControl(control)
    }
    if (this.options.noControl) return

    this._controls.attribution = new U.AttributionControl().addTo(this)
    if (this.options.miniMap) {
      this.whenReady(function () {
        if (this.selected_tilelayer) {
          this._controls.miniMap = new L.Control.MiniMap(this.selected_tilelayer, {
            aimingRectOptions: {
              color: this.getOption('color'),
              fillColor: this.getOption('fillColor'),
              stroke: this.getOption('stroke'),
              fill: this.getOption('fill'),
              weight: this.getOption('weight'),
              opacity: this.getOption('opacity'),
              fillOpacity: this.getOption('fillOpacity'),
            },
          }).addTo(this)
          this._controls.miniMap._miniMap.invalidateSize()
        }
      })
    }
    let name, status, control
    for (let i = 0; i < this.HIDDABLE_CONTROLS.length; i++) {
      name = this.HIDDABLE_CONTROLS[i]
      status = this.getOption(`${name}Control`)
      if (status === false) continue
      control = this._controls[name]
      if (!control) continue
      control.addTo(this)
      if (status === undefined || status === null)
        L.DomUtil.addClass(control._container, 'display-on-more')
      else L.DomUtil.removeClass(control._container, 'display-on-more')
    }
    if (this.getOption('permanentCredit')) this._controls.permanentCredit.addTo(this)
    if (this.getOption('moreControl')) this._controls.more.addTo(this)
    if (this.getOption('scaleControl')) this._controls.scale.addTo(this)
    this._controls.tilelayers.setLayers()
  },

  initDataLayers: async function (datalayers) {
    datalayers = datalayers || this.options.datalayers
    for (const options of datalayers) {
      this.createDataLayer(options)
    }
    await this.loadDataLayers()
  },

  loadDataLayers: async function () {
    this.datalayersLoaded = true
    this.fire('datalayersloaded')
    for (const datalayer of Object.values(this.datalayers)) {
      if (datalayer.showAtLoad()) await datalayer.show()
    }
    this.dataloaded = true
    this.fire('dataloaded')
  },

  indexDatalayers: function () {
    const panes = this.getPane('overlayPane')
    let pane
    this.datalayers_index = []
    for (let i = 0; i < panes.children.length; i++) {
      pane = panes.children[i]
      if (!pane.dataset || !pane.dataset.id) continue
      this.datalayers_index.push(this.datalayers[pane.dataset.id])
    }
    this.onDataLayersChanged()
  },

  onDataLayersChanged: function () {
    if (this.browser) this.browser.update()
    this.caption.refresh()
  },

  ensurePanesOrder: function () {
    this.eachDataLayer((datalayer) => {
      datalayer.bringToTop()
    })
  },

  onceDatalayersLoaded: function (callback, context) {
    // Once datalayers **metadata** have been loaded
    if (this.datalayersLoaded) {
      callback.call(context || this, this)
    } else {
      this.once('datalayersloaded', callback, context)
    }
    return this
  },

  onceDataLoaded: function (callback, context) {
    // Once datalayers **data** have been loaded
    if (this.dataloaded) {
      callback.call(context || this, this)
    } else {
      this.once('dataloaded', callback, context)
    }
    return this
  },

  backupOptions: function () {
    this._backupOptions = L.extend({}, this.options)
    this._backupOptions.tilelayer = L.extend({}, this.options.tilelayer)
    this._backupOptions.limitBounds = L.extend({}, this.options.limitBounds)
    this._backupOptions.permissions = L.extend({}, this.permissions.options)
  },

  resetOptions: function () {
    this.options = L.extend({}, this._backupOptions)
    this.options.tilelayer = L.extend({}, this._backupOptions.tilelayer)
    this.permissions.options = L.extend({}, this._backupOptions.permissions)
  },

  initShortcuts: function () {
    const globalShortcuts = function (e) {
      const key = e.keyCode
      const hasModifier = (e.ctrlKey || e.metaKey) && !e.shiftKey

      /* Generic shortcuts */
      if (key === U.Keys.F && hasModifier) {
        L.DomEvent.stop(e)
        this.search()
      } else if (e.keyCode === U.Keys.ESC) {
        if (this.help.visible()) {
          this.help.hide()
        } else {
          this.panel.close()
          this.editPanel?.close()
          this.fullPanel?.close()
        }
      }

      if (!this.hasEditMode()) return

      /* Edit mode only shortcuts */
      if (key === U.Keys.E && hasModifier && !this.editEnabled) {
        L.DomEvent.stop(e)
        this.enableEdit()
      } else if (key === U.Keys.E && hasModifier && this.editEnabled && !this.isDirty) {
        L.DomEvent.stop(e)
        this.disableEdit()
      }
      if (key === U.Keys.S && hasModifier) {
        L.DomEvent.stop(e)
        if (this.isDirty) {
          this.save()
        }
      }
      if (key === U.Keys.Z && hasModifier && this.isDirty) {
        L.DomEvent.stop(e)
        this.askForReset()
      }
      if (key === U.Keys.M && hasModifier && this.editEnabled) {
        L.DomEvent.stop(e)
        this.editTools.startMarker()
      }
      if (key === U.Keys.P && hasModifier && this.editEnabled) {
        L.DomEvent.stop(e)
        this.editTools.startPolygon()
      }
      if (key === U.Keys.L && hasModifier && this.editEnabled) {
        L.DomEvent.stop(e)
        this.editTools.startPolyline()
      }
      if (key === U.Keys.I && hasModifier && this.editEnabled) {
        L.DomEvent.stop(e)
        this.importer.open()
      }
      if (key === U.Keys.O && hasModifier && this.editEnabled) {
        L.DomEvent.stop(e)
        this.importer.openFiles()
      }
      if (key === U.Keys.H && hasModifier && this.editEnabled) {
        L.DomEvent.stop(e)
        this.help.show('edit')
      }
      if (e.keyCode === U.Keys.ESC) {
        if (this.editEnabled && this.editTools.drawing()) {
          this.editTools.stopDrawing()
        }
        if (this.measureTools.enabled()) this.measureTools.stopDrawing()
      }
    }
    L.DomEvent.addListener(document, 'keydown', globalShortcuts, this)
  },

  initTileLayers: function () {
    this.tilelayers = []
    for (const props of this.options.tilelayers) {
      let layer = this.createTileLayer(props)
      this.tilelayers.push(layer)
      if (
        this.options.tilelayer &&
        this.options.tilelayer.url_template === props.url_template
      ) {
        // Keep control over the displayed attribution for non custom tilelayers
        this.options.tilelayer.attribution = props.attribution
      }
    }
    if (
      this.options.tilelayer &&
      this.options.tilelayer.url_template &&
      this.options.tilelayer.attribution
    ) {
      this.customTilelayer = this.createTileLayer(this.options.tilelayer)
      this.selectTileLayer(this.customTilelayer)
    } else {
      this.selectTileLayer(this.tilelayers[0])
    }
    if (this._controls) this._controls.tilelayers.setLayers()
  },

  createTileLayer: function (tilelayer) {
    return new L.TileLayer(tilelayer.url_template, tilelayer)
  },

  selectTileLayer: function (tilelayer) {
    if (tilelayer === this.selected_tilelayer) {
      return
    }
    try {
      this.addLayer(tilelayer)
      this.fire('baselayerchange', { layer: tilelayer })
      if (this.selected_tilelayer) {
        this.removeLayer(this.selected_tilelayer)
      }
      this.selected_tilelayer = tilelayer
      if (
        !isNaN(this.selected_tilelayer.options.minZoom) &&
        this.getZoom() < this.selected_tilelayer.options.minZoom
      ) {
        this.setZoom(this.selected_tilelayer.options.minZoom)
      }
      if (
        !isNaN(this.selected_tilelayer.options.maxZoom) &&
        this.getZoom() > this.selected_tilelayer.options.maxZoom
      ) {
        this.setZoom(this.selected_tilelayer.options.maxZoom)
      }
    } catch (e) {
      console.error(e)
      this.removeLayer(tilelayer)
      this.ui.alert({
        content: `${L._('Error in the tilelayer URL')}: ${tilelayer._url}`,
        level: 'error',
      })
      // Users can put tilelayer URLs by hand, and if they add wrong {variable},
      // Leaflet throw an error, and then the map is no more editable
    }
    this.setOverlay()
  },

  eachTileLayer: function (callback, context) {
    const urls = []
    const callOne = (layer) => {
      // Prevent adding a duplicate background,
      // while adding selected/custom on top of the list
      const url = layer.options.url_template
      if (urls.indexOf(url) !== -1) return
      callback.call(context, layer)
      urls.push(url)
    }
    if (this.selected_tilelayer) callOne(this.selected_tilelayer)
    if (this.customTilelayer) callOne(this.customTilelayer)
    this.tilelayers.forEach(callOne)
  },

  setOverlay: function () {
    if (!this.options.overlay || !this.options.overlay.url_template) return
    const overlay = this.createTileLayer(this.options.overlay)
    try {
      this.addLayer(overlay)
      if (this.overlay) this.removeLayer(this.overlay)
      this.overlay = overlay
    } catch (e) {
      this.removeLayer(overlay)
      console.error(e)
      this.ui.alert({
        content: `${L._('Error in the overlay URL')}: ${overlay._url}`,
        level: 'error',
      })
    }
  },

  _setDefaultCenter: function () {
    this.options.center = this.latLng(this.options.center)
    this.setView(this.options.center, this.options.zoom)
  },

  hasData: function () {
    for (const datalayer of this.datalayers_index) {
      if (datalayer.hasData()) return true
    }
  },

  fitDataBounds: function () {
    const bounds = this.getLayersBounds()
    if (!this.hasData() || !bounds.isValid()) return false
    this.fitBounds(bounds)
  },

  initCenter: function () {
    this._setDefaultCenter()
    if (this.options.hash) this.addHash()
    if (this.options.hash && this._hash.parseHash(location.hash)) {
      // FIXME An invalid hash will cause the load to fail
      this._hash.update()
    } else if (this.options.defaultView === 'locate' && !this.options.noControl) {
      this._controls.locate.start()
    } else if (this.options.defaultView === 'data') {
      this.onceDataLoaded(this.fitDataBounds)
    } else if (this.options.defaultView === 'latest') {
      this.onceDataLoaded(() => {
        if (!this.hasData()) return
        const datalayer = this.firstVisibleDatalayer()
        let feature
        if (datalayer) {
          const feature = datalayer.getFeatureByIndex(-1)
          if (feature) {
            feature.zoomTo({ callback: this.options.noControl ? null : feature.view })
            return
          }
        }
      })
    }
  },

  latLng: function (a, b, c) {
    // manage geojson case and call original method
    if (!(a instanceof L.LatLng) && a.coordinates) {
      // Guess it's a geojson
      a = [a.coordinates[1], a.coordinates[0]]
    }
    return L.latLng(a, b, c)
  },

  handleLimitBounds: function () {
    const south = parseFloat(this.options.limitBounds.south),
      west = parseFloat(this.options.limitBounds.west),
      north = parseFloat(this.options.limitBounds.north),
      east = parseFloat(this.options.limitBounds.east)
    if (!isNaN(south) && !isNaN(west) && !isNaN(north) && !isNaN(east)) {
      const bounds = L.latLngBounds([
        [south, west],
        [north, east],
      ])
      this.options.minZoom = this.getBoundsZoom(bounds, false)
      try {
        this.setMaxBounds(bounds)
      } catch (e) {
        // Unusable bounds, like -2 -2 -2 -2?
        console.error('Error limiting bounds', e)
      }
    } else {
      this.options.minZoom = 0
      this.setMaxBounds()
    }
  },

  setMaxBounds: function (bounds) {
    // Hack. Remove me when fix is released:
    // https://github.com/Leaflet/Leaflet/pull/4494
    bounds = L.latLngBounds(bounds)

    if (!bounds.isValid()) {
      this.options.maxBounds = null
      return this.off('moveend', this._panInsideMaxBounds)
    }
    return L.Map.prototype.setMaxBounds.call(this, bounds)
  },

  createDataLayer: function (datalayer) {
    datalayer = datalayer || {
      name: `${L._('Layer')} ${this.datalayers_index.length + 1}`,
    }
    return new U.DataLayer(this, datalayer)
  },

  newDataLayer: function () {
    const datalayer = this.createDataLayer({})
    datalayer.edit()
  },

  getDefaultOption: function (option) {
    return U.SCHEMA[option] && U.SCHEMA[option].default
  },

  getOption: function (option) {
    if (U.Utils.usableOption(this.options, option)) return this.options[option]
    return this.getDefaultOption(option)
  },

  updateExtent: function () {
    this.options.center = this.getCenter()
    this.options.zoom = this.getZoom()
    this.isDirty = true
    this._default_extent = false
    if (this.options.umap_id) {
      // We do not want an extra message during the map creation
      // to avoid the double notification/alert.
      this.ui.alert({
        content: L._('The zoom and center have been modified.'),
        level: 'info',
      })
    }
  },

  updateTileLayers: function () {
    const self = this,
      callback = (tilelayer) => {
        self.options.tilelayer = tilelayer.toJSON()
        self.isDirty = true
      }
    if (this._controls.tilelayersChooser)
      this._controls.tilelayersChooser.openSwitcher({
        callback: callback,
        className: 'dark',
      })
  },

  toGeoJSON: function () {
    let features = []
    this.eachDataLayer((datalayer) => {
      if (datalayer.isVisible()) {
        features = features.concat(datalayer.featuresToGeoJSON())
      }
    })
    const geojson = {
      type: 'FeatureCollection',
      features: features,
    }
    return geojson
  },

  eachFeature: function (callback, context) {
    this.eachDataLayer((datalayer) => {
      if (datalayer.isVisible()) datalayer.eachFeature(callback, context)
    })
  },

  processFileToImport: function (file, layer, type) {
    type = type || U.Utils.detectFileType(file)
    if (!type) {
      this.ui.alert({
        content: L._('Unable to detect format of file {filename}', {
          filename: file.name,
        }),
        level: 'error',
      })
      return
    }
    if (type === 'umap') {
      this.importFromFile(file, 'umap')
    } else {
      if (!layer) layer = this.createDataLayer({ name: file.name })
      layer.importFromFile(file, type)
    }
  },

  importRaw: function (rawData) {
    const importedData = JSON.parse(rawData)

    let mustReindex = false

    for (const option of Object.keys(U.SCHEMA)) {
      if (typeof importedData.properties[option] !== 'undefined') {
        this.options[option] = importedData.properties[option]
        if (option === 'sortKey') mustReindex = true
      }
    }

    if (importedData.geometry) this.options.center = this.latLng(importedData.geometry)
    const self = this
    importedData.layers.forEach((geojson) => {
      delete geojson._umap_options['id'] // Never trust an id at this stage
      const dataLayer = self.createDataLayer(geojson._umap_options)
      dataLayer.fromUmapGeoJSON(geojson)
    })

    this.initTileLayers()
    this.renderControls()
    this.handleLimitBounds()
    this.eachDataLayer((datalayer) => {
      if (mustReindex) datalayer.reindex()
      datalayer.redraw()
    })
    this.fire('postsync')
    this.isDirty = true
  },

  importFromFile: function (file) {
    const reader = new FileReader()
    reader.readAsText(file)
    const self = this
    reader.onload = (e) => {
      const rawData = e.target.result
      try {
        self.importRaw(rawData)
      } catch (e) {
        console.error('Error importing data', e)
        self.ui.alert({
          content: L._('Invalid umap data in {filename}', { filename: file.name }),
          level: 'error',
        })
      }
    }
  },

  openBrowser: function (mode) {
    this.onceDatalayersLoaded(() => this.browser.open(mode))
  },

  openCaption: function () {
    this.onceDatalayersLoaded(() => this.caption.open())
  },

  eachDataLayer: function (method, context) {
    for (let i = 0; i < this.datalayers_index.length; i++) {
      method.call(context, this.datalayers_index[i])
    }
  },

  eachDataLayerReverse: function (method, context, filter) {
    for (let i = this.datalayers_index.length - 1; i >= 0; i--) {
      if (filter && !filter.call(context, this.datalayers_index[i])) continue
      method.call(context, this.datalayers_index[i])
    }
  },

  eachBrowsableDataLayer: function (method, context) {
    this.eachDataLayerReverse(method, context, (d) => d.allowBrowse())
  },

  eachVisibleDataLayer: function (method, context) {
    this.eachDataLayerReverse(method, context, (d) => d.isVisible())
  },

  findDataLayer: function (method, context) {
    for (let i = this.datalayers_index.length - 1; i >= 0; i--) {
      if (method.call(context, this.datalayers_index[i]))
        return this.datalayers_index[i]
    }
  },

  backup: function () {
    this.backupOptions()
    this._datalayers_index_bk = [].concat(this.datalayers_index)
  },

  reset: function () {
    if (this.editTools) this.editTools.stopDrawing()
    this.resetOptions()
    this.datalayers_index = [].concat(this._datalayers_index_bk)
    this.dirty_datalayers.slice().forEach((datalayer) => {
      if (datalayer.isDeleted) datalayer.connectToMap()
      datalayer.reset()
    })
    this.ensurePanesOrder()
    this.dirty_datalayers = []
    this.initTileLayers()
    this.isDirty = false
    this.onDataLayersChanged()
  },

  checkDirty: function () {
    this._container.classList.toggle('umap-is-dirty', this.isDirty)
  },

  addDirtyDatalayer: function (datalayer) {
    if (this.dirty_datalayers.indexOf(datalayer) === -1) {
      this.dirty_datalayers.push(datalayer)
      this.isDirty = true
    }
  },

  removeDirtyDatalayer: function (datalayer) {
    if (this.dirty_datalayers.indexOf(datalayer) !== -1) {
      this.dirty_datalayers.splice(this.dirty_datalayers.indexOf(datalayer), 1)
      this.checkDirty()
    }
  },

  continueSaving: function () {
    if (this.dirty_datalayers.length) this.dirty_datalayers[0].save()
    else this.fire('saved')
  },

  exportOptions: function () {
    const properties = {}
    for (const option of Object.keys(U.SCHEMA)) {
      if (typeof this.options[option] !== 'undefined') {
        properties[option] = this.options[option]
      }
    }
    return properties
  },

  saveSelf: async function () {
    const geojson = {
      type: 'Feature',
      geometry: this.geometry(),
      properties: this.exportOptions(),
    }
    const formData = new FormData()
    formData.append('name', this.options.name)
    formData.append('center', JSON.stringify(this.geometry()))
    formData.append('settings', JSON.stringify(geojson))
    const uri = this.urls.get('map_save', { map_id: this.options.umap_id })
    const [data, response, error] = await this.server.post(uri, {}, formData)
    // FIXME: login_required response will not be an error, so it will not
    // stop code while it should
    if (!error) {
      let duration = 3000,
        alert = { content: L._('Map has been saved!'), level: 'info' }
      if (!this.options.umap_id) {
        alert.content = L._('Congratulations, your map has been created!')
        this.options.umap_id = data.id
        this.permissions.setOptions(data.permissions)
        this.permissions.commit()
        if (data.permissions && data.permissions.anonymous_edit_url) {
          alert.duration = Infinity
          alert.content =
            L._(
              'Your map has been created! As you are not logged in, here is your secret link to edit the map, please keep it safe:'
            ) + `<br>${data.permissions.anonymous_edit_url}`

          alert.actions = [
            {
              label: L._('Copy link'),
              callback: () => {
                L.Util.copyToClipboard(data.permissions.anonymous_edit_url)
                this.ui.alert({
                  content: L._('Secret edit link copied to clipboard!'),
                  level: 'info',
                })
              },
              callbackContext: this,
            },
          ]
          if (this.options.urls.map_send_edit_link) {
            alert.actions.push({
              label: L._('Send me the link'),
              input: L._('Email'),
              callback: this.sendEditLink,
              callbackContext: this,
            })
          }
        }
      } else if (!this.permissions.isDirty) {
        // Do not override local changes to permissions,
        // but update in case some other editors changed them in the meantime.
        this.permissions.setOptions(data.permissions)
        this.permissions.commit()
      }
      // Update URL in case the name has changed.
      if (history && history.pushState)
        history.pushState({}, this.options.name, data.url)
      else window.location = data.url
      alert.content = data.info || alert.content
      this.once('saved', () => this.ui.alert(alert))
      this.permissions.save()
    }
  },

  save: function () {
    if (!this.isDirty) return
    if (this._default_extent) this.updateExtent()
    this.backup()
    this.once('saved', () => {
      this.isDirty = false
    })
    if (this.options.editMode === 'advanced') {
      // Only save the map if the user has the rights to do so.
      this.saveSelf()
    } else {
      this.permissions.save()
    }
  },

  sendEditLink: async function () {
    const input = this.ui._alert.querySelector('input')
    const email = input.value

    const formData = new FormData()
    formData.append('email', email)

    const url = this.urls.get('map_send_edit_link', { map_id: this.options.umap_id })
    await this.server.post(url, {}, formData)
  },

  star: async function () {
    if (!this.options.umap_id)
      return this.ui.alert({
        content: L._('Please save the map first'),
        level: 'error',
      })
    const url = this.urls.get('map_star', { map_id: this.options.umap_id })
    const [data, response, error] = await this.server.post(url)
    if (!error) {
      this.options.starred = data.starred
      let msg = data.starred
        ? L._('Map has been starred')
        : L._('Map has been unstarred')
      this.ui.alert({ content: msg, level: 'info' })
      this.renderControls()
    }
  },

  geometry: function () {
    /* Return a GeoJSON geometry Object */
    const latlng = this.latLng(this.options.center || this.getCenter())
    return {
      type: 'Point',
      coordinates: [latlng.lng, latlng.lat],
    }
  },

  firstVisibleDatalayer: function () {
    return this.findDataLayer((datalayer) => {
      if (datalayer.isVisible()) return true
    })
  },

  // TODO: allow to control the default datalayer
  // (edit and viewing)
  // cf https://github.com/umap-project/umap/issues/585
  defaultEditDataLayer: function () {
    let datalayer, fallback
    datalayer = this.lastUsedDataLayer
    if (
      datalayer &&
      !datalayer.isDataReadOnly() &&
      datalayer.isBrowsable() &&
      datalayer.isVisible()
    ) {
      return datalayer
    }
    datalayer = this.findDataLayer((datalayer) => {
      if (!datalayer.isDataReadOnly() && datalayer.isBrowsable()) {
        fallback = datalayer
        if (datalayer.isVisible()) return true
      }
    })
    if (datalayer) return datalayer
    if (fallback) {
      // No datalayer visible, let's force one
      fallback.show()
      return fallback
    }
    return this.createDataLayer()
  },

  getDataLayerByUmapId: function (umap_id) {
    return this.findDataLayer((d) => d.umap_id == umap_id)
  },

  _editControls: function (container) {
    let UIFields = []
    for (let i = 0; i < this.HIDDABLE_CONTROLS.length; i++) {
      UIFields.push(`options.${this.HIDDABLE_CONTROLS[i]}Control`)
    }
    UIFields = UIFields.concat([
      'options.moreControl',
      'options.scrollWheelZoom',
      'options.miniMap',
      'options.scaleControl',
      'options.onLoadPanel',
      'options.defaultView',
      'options.displayPopupFooter',
      'options.captionBar',
      'options.captionMenus',
    ])
    builder = new U.FormBuilder(this, UIFields)
    const controlsOptions = L.DomUtil.createFieldset(
      container,
      L._('User interface options')
    )
    controlsOptions.appendChild(builder.build())
  },

  _editShapeProperties: function (container) {
    const shapeOptions = [
      'options.color',
      'options.iconClass',
      'options.iconUrl',
      'options.iconOpacity',
      'options.opacity',
      'options.weight',
      'options.fill',
      'options.fillColor',
      'options.fillOpacity',
      'options.smoothFactor',
      'options.dashArray',
    ]

    builder = new U.FormBuilder(this, shapeOptions)
    const defaultShapeProperties = L.DomUtil.createFieldset(
      container,
      L._('Default shape properties')
    )
    defaultShapeProperties.appendChild(builder.build())
  },

  _editDefaultProperties: function (container) {
    const optionsFields = [
      'options.zoomTo',
      ['options.easing', { handler: 'Switch', label: L._('Animated transitions') }],
      'options.labelKey',
      [
        'options.sortKey',
        {
          handler: 'BlurInput',
          helpEntries: 'sortKey',
          placeholder: L._('Default: name'),
          label: L._('Sort key'),
          inheritable: true,
        },
      ],
      [
        'options.filterKey',
        {
          handler: 'Input',
          helpEntries: 'filterKey',
          placeholder: L._('Default: name'),
          label: L._('Search keys'),
          inheritable: true,
        },
      ],
      [
        'options.facetKey',
        {
          handler: 'BlurInput',
          helpEntries: 'facetKey',
          placeholder: L._('Example: key1,key2|Label 2,key3|Label 3|checkbox'),
          label: L._('Filters keys'),
        },
      ],
      [
        'options.slugKey',
        {
          handler: 'BlurInput',
          helpEntries: 'slugKey',
          placeholder: L._('Default: name'),
          label: L._('Feature identifier key'),
        },
      ],
    ]

    builder = new U.FormBuilder(this, optionsFields)
    const defaultProperties = L.DomUtil.createFieldset(
      container,
      L._('Default properties')
    )
    defaultProperties.appendChild(builder.build())
  },

  _editInteractionsProperties: function (container) {
    const popupFields = [
      'options.popupShape',
      'options.popupTemplate',
      'options.popupContentTemplate',
      'options.showLabel',
      'options.labelDirection',
      'options.labelInteractive',
      'options.outlinkTarget',
    ]
    builder = new U.FormBuilder(this, popupFields)
    const popupFieldset = L.DomUtil.createFieldset(
      container,
      L._('Default interaction options')
    )
    popupFieldset.appendChild(builder.build())
  },

  _editTilelayer: function (container) {
    if (!U.Utils.isObject(this.options.tilelayer)) {
      this.options.tilelayer = {}
    }
    const tilelayerFields = [
      [
        'options.tilelayer.name',
        { handler: 'BlurInput', placeholder: L._('display name') },
      ],
      [
        'options.tilelayer.url_template',
        {
          handler: 'BlurInput',
          helpText: `${L._('Supported scheme')}: http://{s}.domain.com/{z}/{x}/{y}.png`,
          placeholder: 'url',
          type: 'url',
        },
      ],
      [
        'options.tilelayer.maxZoom',
        {
          handler: 'BlurIntInput',
          placeholder: L._('max zoom'),
          min: 0,
          max: this.options.maxZoomLimit,
        },
      ],
      [
        'options.tilelayer.minZoom',
        {
          handler: 'BlurIntInput',
          placeholder: L._('min zoom'),
          min: 0,
          max: this.options.maxZoomLimit,
        },
      ],
      [
        'options.tilelayer.attribution',
        { handler: 'BlurInput', placeholder: L._('attribution') },
      ],
      ['options.tilelayer.tms', { handler: 'Switch', label: L._('TMS format') }],
    ]
    const customTilelayer = L.DomUtil.createFieldset(
      container,
      L._('Custom background')
    )
    builder = new U.FormBuilder(this, tilelayerFields)
    customTilelayer.appendChild(builder.build())
  },

  _editOverlay: function (container) {
    if (!U.Utils.isObject(this.options.overlay)) {
      this.options.overlay = {}
    }
    const overlayFields = [
      [
        'options.overlay.url_template',
        {
          handler: 'BlurInput',
          helpText: `${L._('Supported scheme')}: http://{s}.domain.com/{z}/{x}/{y}.png`,
          placeholder: 'url',
          helpText: L._('Background overlay url'),
          type: 'url',
        },
      ],
      [
        'options.overlay.maxZoom',
        {
          handler: 'BlurIntInput',
          placeholder: L._('max zoom'),
          min: 0,
          max: this.options.maxZoomLimit,
        },
      ],
      [
        'options.overlay.minZoom',
        {
          handler: 'BlurIntInput',
          placeholder: L._('min zoom'),
          min: 0,
          max: this.options.maxZoomLimit,
        },
      ],
      [
        'options.overlay.attribution',
        { handler: 'BlurInput', placeholder: L._('attribution') },
      ],
      [
        'options.overlay.opacity',
        { handler: 'Range', min: 0, max: 1, step: 0.1, label: L._('Opacity') },
      ],
      ['options.overlay.tms', { handler: 'Switch', label: L._('TMS format') }],
    ]
    const overlay = L.DomUtil.createFieldset(container, L._('Custom overlay'))
    builder = new U.FormBuilder(this, overlayFields)
    overlay.appendChild(builder.build())
  },

  _editBounds: function (container) {
    if (!U.Utils.isObject(this.options.limitBounds)) {
      this.options.limitBounds = {}
    }
    const limitBounds = L.DomUtil.createFieldset(container, L._('Limit bounds'))
    const boundsFields = [
      [
        'options.limitBounds.south',
        { handler: 'BlurFloatInput', placeholder: L._('max South') },
      ],
      [
        'options.limitBounds.west',
        { handler: 'BlurFloatInput', placeholder: L._('max West') },
      ],
      [
        'options.limitBounds.north',
        { handler: 'BlurFloatInput', placeholder: L._('max North') },
      ],
      [
        'options.limitBounds.east',
        { handler: 'BlurFloatInput', placeholder: L._('max East') },
      ],
    ]
    const boundsBuilder = new U.FormBuilder(this, boundsFields)
    limitBounds.appendChild(boundsBuilder.build())
    const boundsButtons = L.DomUtil.create('div', 'button-bar half', limitBounds)
    L.DomUtil.createButton(
      'button',
      boundsButtons,
      L._('Use current bounds'),
      function () {
        const bounds = this.getBounds()
        this.options.limitBounds.south = L.Util.formatNum(bounds.getSouth())
        this.options.limitBounds.west = L.Util.formatNum(bounds.getWest())
        this.options.limitBounds.north = L.Util.formatNum(bounds.getNorth())
        this.options.limitBounds.east = L.Util.formatNum(bounds.getEast())
        boundsBuilder.fetchAll()
        this.isDirty = true
        this.handleLimitBounds()
      },
      this
    )
    L.DomUtil.createButton(
      'button',
      boundsButtons,
      L._('Empty'),
      function () {
        this.options.limitBounds.south = null
        this.options.limitBounds.west = null
        this.options.limitBounds.north = null
        this.options.limitBounds.east = null
        boundsBuilder.fetchAll()
        this.isDirty = true
        this.handleLimitBounds()
      },
      this
    )
  },

  _editSlideshow: function (container) {
    const slideshow = L.DomUtil.createFieldset(container, L._('Slideshow'))
    const slideshowFields = [
      [
        'options.slideshow.active',
        { handler: 'Switch', label: L._('Activate slideshow mode') },
      ],
      [
        'options.slideshow.delay',
        {
          handler: 'SlideshowDelay',
          helpText: L._('Delay between two transitions when in play mode'),
        },
      ],
      [
        'options.slideshow.easing',
        { handler: 'Switch', label: L._('Animated transitions'), inheritable: true },
      ],
      [
        'options.slideshow.autoplay',
        { handler: 'Switch', label: L._('Autostart when map is loaded') },
      ],
    ]
    const slideshowHandler = function () {
      this.slideshow.setOptions(this.options.slideshow)
    }
    const slideshowBuilder = new U.FormBuilder(this, slideshowFields, {
      callback: slideshowHandler,
      callbackContext: this,
    })
    slideshow.appendChild(slideshowBuilder.build())
  },

  _advancedActions: function (container) {
    const advancedActions = L.DomUtil.createFieldset(container, L._('Advanced actions'))
    const advancedButtons = L.DomUtil.create('div', 'button-bar half', advancedActions)
    if (this.permissions.isOwner()) {
      L.DomUtil.createButton(
        'button umap-delete',
        advancedButtons,
        L._('Delete'),
        this.del,
        this
      )
      L.DomUtil.createButton(
        'button umap-empty',
        advancedButtons,
        L._('Empty'),
        this.empty,
        this
      )
    }
    L.DomUtil.createButton(
      'button umap-clone',
      advancedButtons,
      L._('Clone this map'),
      this.clone,
      this
    )
    L.DomUtil.createButton(
      'button umap-empty',
      advancedButtons,
      L._('Delete all layers'),
      this.empty,
      this
    )
    L.DomUtil.createButton(
      'button umap-download',
      advancedButtons,
      L._('Open share & download panel'),
      this.share.open,
      this.share
    )
  },

  editCaption: function () {
    if (!this.editEnabled) return
    if (this.options.editMode !== 'advanced') return
    const container = L.DomUtil.create('div', 'umap-edit-container'),
      metadataFields = ['options.name', 'options.description'],
      title = L.DomUtil.create('h3', '', container)
    title.textContent = L._('Edit map details')
    const builder = new U.FormBuilder(this, metadataFields, {
      className: 'map-metadata',
    })
    const form = builder.build()
    container.appendChild(form)

    const credits = L.DomUtil.createFieldset(container, L._('Credits'))
    const creditsFields = [
      'options.licence',
      'options.shortCredit',
      'options.longCredit',
      'options.permanentCredit',
      'options.permanentCreditBackground',
    ]
    const creditsBuilder = new U.FormBuilder(this, creditsFields)
    credits.appendChild(creditsBuilder.build())
    this.editPanel.open({ content: container })
  },

  edit: function () {
    if (!this.editEnabled) return
    if (this.options.editMode !== 'advanced') return
    const container = L.DomUtil.create('div')
    L.DomUtil.createTitle(container, L._('Map advanced properties'), 'icon-settings')
    this._editControls(container)
    this._editShapeProperties(container)
    this._editDefaultProperties(container)
    this._editInteractionsProperties(container)
    this._editTilelayer(container)
    this._editOverlay(container)
    this._editBounds(container)
    this._editSlideshow(container)
    this._advancedActions(container)

    this.editPanel.open({ content: container, className: 'dark' })
  },

  enableEdit: function () {
    L.DomUtil.addClass(document.body, 'umap-edit-enabled')
    this.editEnabled = true
    this.drop.enable()
    this.fire('edit:enabled')
  },

  disableEdit: function () {
    if (this.isDirty) return
    this.drop.disable()
    L.DomUtil.removeClass(document.body, 'umap-edit-enabled')
    this.editedFeature = null
    this.editEnabled = false
    this.fire('edit:disabled')
    this.editPanel.close()
    this.fullPanel.close()
  },

  hasEditMode: function () {
    return this.options.editMode === 'simple' || this.options.editMode === 'advanced'
  },

  getDisplayName: function () {
    return this.options.name || L._('Untitled map')
  },

  initCaptionBar: function () {
    const container = L.DomUtil.create(
        'div',
        'umap-caption-bar',
        this._controlContainer
      ),
      name = L.DomUtil.create('h3', '', container)
    L.DomEvent.disableClickPropagation(container)
    this.permissions.addOwnerLink('span', container)
    if (this.getOption('captionMenus')) {
      L.DomUtil.createButton(
        'umap-about-link flat',
        container,
        L._('About'),
        this.openCaption,
        this
      )
      L.DomUtil.createButton(
        'umap-open-browser-link flat',
        container,
        L._('Browse data'),
        () => this.openBrowser('data')
      )
      if (this.options.facetKey) {
        L.DomUtil.createButton(
          'umap-open-filter-link flat',
          container,
          L._('Filter data'),
          () => this.openBrowser('filters')
        )
      }
    }
    const setName = function () {
      name.textContent = this.getDisplayName()
    }
    L.bind(setName, this)()
    this.on('postsync', L.bind(setName, this))
    this.onceDatalayersLoaded(function () {
      this.slideshow.renderToolbox(container)
    })
  },

  askForReset: function (e) {
    if (!confirm(L._('Are you sure you want to cancel your changes?'))) return
    this.reset()
    this.disableEdit()
  },

  startMarker: function () {
    return this.editTools.startMarker()
  },

  startPolyline: function () {
    return this.editTools.startPolyline()
  },

  startPolygon: function () {
    return this.editTools.startPolygon()
  },

  del: async function () {
    if (confirm(L._('Are you sure you want to delete this map?'))) {
      const url = this.urls.get('map_delete', { map_id: this.options.umap_id })
      const [data, response, error] = await this.server.post(url)
      if (data.redirect) window.location = data.redirect
    }
  },

  clone: async function () {
    if (
      confirm(L._('Are you sure you want to clone this map and all its datalayers?'))
    ) {
      const url = this.urls.get('map_clone', { map_id: this.options.umap_id })
      const [data, response, error] = await this.server.post(url)
      if (data.redirect) window.location = data.redirect
    }
  },

  empty: function () {
    this.eachDataLayerReverse((datalayer) => {
      datalayer._delete()
    })
  },

  initLoader: function () {
    this.loader = new L.Control.Loading()
    this.loader.onAdd(this)
  },

  initContextMenu: function () {
    this.contextmenu = new U.ContextMenu(this)
    this.contextmenu.enable()
  },

  setContextMenuItems: function (e) {
    let items = []
    if (this._zoom !== this.getMaxZoom()) {
      items.push({
        text: L._('Zoom in'),
        callback: function () {
          this.zoomIn()
        },
      })
    }
    if (this._zoom !== this.getMinZoom()) {
      items.push({
        text: L._('Zoom out'),
        callback: function () {
          this.zoomOut()
        },
      })
    }
    if (e && e.relatedTarget) {
      if (e.relatedTarget.getContextMenuItems) {
        items = items.concat(e.relatedTarget.getContextMenuItems(e))
      }
    }
    if (this.hasEditMode()) {
      items.push('-')
      if (this.editEnabled) {
        if (!this.isDirty) {
          items.push({
            text: this.help.displayLabel('STOP_EDIT'),
            callback: this.disableEdit,
          })
        }
        if (this.options.enableMarkerDraw) {
          items.push({
            text: this.help.displayLabel('DRAW_MARKER'),
            callback: this.startMarker,
            context: this,
          })
        }
        if (this.options.enablePolylineDraw) {
          items.push({
            text: this.help.displayLabel('DRAW_POLYGON'),
            callback: this.startPolygon,
            context: this,
          })
        }
        if (this.options.enablePolygonDraw) {
          items.push({
            text: this.help.displayLabel('DRAW_LINE'),
            callback: this.startPolyline,
            context: this,
          })
        }
        items.push('-')
        items.push({
          text: L._('Help'),
          callback: function () {
            this.help.show('edit')
          },
        })
      } else {
        items.push({
          text: this.help.displayLabel('TOGGLE_EDIT'),
          callback: this.enableEdit,
        })
      }
    }
    items.push(
      '-',
      {
        text: L._('See layers'),
        callback: () => this.openBrowser('layers'),
      },
      {
        text: L._('Browse data'),
        callback: () => this.openBrowser('data'),
      }
    )
    if (this.options.facetKey) {
      items.push({
        text: L._('Filter data'),
        callback: () => this.openBrowser('filters'),
      })
    }
    items.push(
      {
        text: L._('About'),
        callback: this.openCaption,
      },
      {
        text: this.help.displayLabel('SEARCH'),
        callback: this.search,
      }
    )
    if (this.options.urls.routing) {
      items.push('-', {
        text: L._('Directions from here'),
        callback: this.openExternalRouting,
      })
    }
    if (this.options.urls.edit_in_osm) {
      items.push('-', {
        text: L._('Edit in OpenStreetMap'),
        callback: this.editInOSM,
      })
    }
    this.options.contextmenuItems = items
  },

  editInOSM: function (e) {
    const url = this.urls.get('edit_in_osm', {
      lat: e.latlng.lat,
      lng: e.latlng.lng,
      zoom: Math.max(this.getZoom(), 16),
    })
    if (url) window.open(url)
  },

  openExternalRouting: function (e) {
    const url = this.urls.get('routing', {
      lat: e.latlng.lat,
      lng: e.latlng.lng,
      locale: L.getLocale(),
      zoom: this.getZoom(),
    })
    if (url) window.open(url)
  },

  getMap: function () {
    return this
  },

  getGeoContext: function () {
    const context = {
      bbox: this.getBounds().toBBoxString(),
      north: this.getBounds().getNorthEast().lat,
      east: this.getBounds().getNorthEast().lng,
      south: this.getBounds().getSouthWest().lat,
      west: this.getBounds().getSouthWest().lng,
      lat: this.getCenter().lat,
      lng: this.getCenter().lng,
      zoom: this.getZoom(),
    }
    context.left = context.west
    context.bottom = context.south
    context.right = context.east
    context.top = context.north
    return context
  },

  localizeUrl: function (url) {
    return U.Utils.greedyTemplate(url, this.getGeoContext(), true)
  },

  proxyUrl: function (url, ttl) {
    if (this.options.urls.ajax_proxy) {
      url = U.Utils.greedyTemplate(this.options.urls.ajax_proxy, {
        url: encodeURIComponent(url),
        ttl: ttl,
      })
    }
    return url
  },

  closeInplaceToolbar: function () {
    const toolbar = this._toolbars[L.Toolbar.Popup._toolbar_class_id]
    if (toolbar) toolbar.remove()
  },

  search: function () {
    if (this._controls.search) this._controls.search.open()
  },

  getFilterKeys: function () {
    return (this.options.filterKey || this.options.sortKey || 'name').split(',')
  },

  getLayersBounds: function () {
    const bounds = new L.latLngBounds()
    this.eachBrowsableDataLayer((d) => {
      if (d.isVisible()) bounds.extend(d.layer.getBounds())
    })
    return bounds
  },
})
