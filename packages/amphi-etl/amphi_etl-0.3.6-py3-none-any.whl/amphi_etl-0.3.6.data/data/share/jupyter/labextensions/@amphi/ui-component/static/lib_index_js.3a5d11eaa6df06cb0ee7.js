"use strict";
(self["webpackChunk_amphi_ui_component"] = self["webpackChunk_amphi_ui_component"] || []).push([["lib_index_js"],{

/***/ "../../node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!*******************************************************************!*\
  !*** ../../node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \*******************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/sourceMaps.js */ "../../node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_output_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../../../node_modules/css-loader/dist/cjs.js!./output.css */ "../../node_modules/css-loader/dist/cjs.js!./style/output.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_output_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
`, "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":"AAAA;;;8EAG8E","sourcesContent":["/*-----------------------------------------------------------------------------\n| Copyright (c) Jupyter Development Team.\n| Distributed under the terms of the Modified BSD License.\n|----------------------------------------------------------------------------*/\n\n@import url('output.css');\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./lib/BrowseFileDialog.js":
/*!*********************************!*\
  !*** ./lib/BrowseFileDialog.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   showBrowseFileDialog: () => (/* binding */ showBrowseFileDialog)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/*
 * Copyright 2018-2023 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */



const BROWSE_FILE_CLASS = 'elyra-browseFileDialog';
const BROWSE_FILE_OPEN_CLASS = 'elyra-browseFileDialog-open';
/**
 * Breadcrumbs widget for browse file dialog body.
 */
class BrowseFileDialogBreadcrumbs extends _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.BreadCrumbs {
    constructor(options) {
        super(options);
        this.model = options.model;
        this.rootPath = options.rootPath;
    }
    onUpdateRequest(msg) {
        super.onUpdateRequest(msg);
        const contents = this.model.manager.services.contents;
        const localPath = contents.localPath(this.model.path);
        // if 'rootPath' is defined prevent navigating to it's parent/grandparent directories
        if (localPath && this.rootPath && localPath.indexOf(this.rootPath) === 0) {
            const breadcrumbs = document.querySelectorAll('.elyra-browseFileDialog .jp-BreadCrumbs > span[title]');
            breadcrumbs.forEach((crumb) => {
                var _a;
                if (crumb.title.indexOf((_a = this.rootPath) !== null && _a !== void 0 ? _a : '') === 0) {
                    crumb.className = crumb.className
                        .replace('elyra-BreadCrumbs-disabled', '')
                        .trim();
                }
                else if (crumb.className.indexOf('elyra-BreadCrumbs-disabled') === -1) {
                    crumb.className += ' elyra-BreadCrumbs-disabled';
                }
            });
        }
    }
}
/**
 * Browse file widget for dialog body
 */
class BrowseFileDialog extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor(props) {
        super(props);
        this.model = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.FilterFileBrowserModel({
            manager: props.manager,
            filter: props.filter
        });
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout());
        this.directoryListing = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.DirListing({
            model: this.model
        });
        this.acceptFileOnDblClick = props.acceptFileOnDblClick;
        this.multiselect = props.multiselect;
        this.includeDir = props.includeDir;
        this.dirListingHandleEvent = this.directoryListing.handleEvent;
        this.directoryListing.handleEvent = (event) => {
            this.handleEvent(event);
        };
        this.breadCrumbs = new BrowseFileDialogBreadcrumbs({
            model: this.model,
            rootPath: props.rootPath
        });
        layout.addWidget(this.breadCrumbs);
        layout.addWidget(this.directoryListing);
    }
    static async init(options) {
        const browseFileDialog = new BrowseFileDialog(options);
        if (options.startPath) {
            if (!options.rootPath ||
                options.startPath.indexOf(options.rootPath) === 0) {
                await browseFileDialog.model.cd(options.startPath);
            }
        }
        else if (options.rootPath) {
            await browseFileDialog.model.cd(options.rootPath);
        }
        return browseFileDialog;
    }
    getValue() {
        const selected = [];
        let item = null;
        for (const item of this.directoryListing.selectedItems()) {
            if (this.includeDir || item.type !== 'directory') {
                selected.push(item);
            }
        }
        return selected;
    }
    handleEvent(event) {
        let modifierKey = false;
        if (event instanceof MouseEvent) {
            modifierKey =
                event.shiftKey || event.metaKey;
        }
        else if (event instanceof KeyboardEvent) {
            modifierKey =
                event.shiftKey || event.metaKey;
        }
        switch (event.type) {
            case 'keydown':
            case 'keyup':
            case 'mousedown':
            case 'mouseup':
            case 'click':
                if (this.multiselect || !modifierKey) {
                    this.dirListingHandleEvent.call(this.directoryListing, event);
                }
                break;
            case 'dblclick': {
                const clickedItem = this.directoryListing.modelForClick(event);
                if ((clickedItem === null || clickedItem === void 0 ? void 0 : clickedItem.type) === 'directory') {
                    this.dirListingHandleEvent.call(this.directoryListing, event);
                }
                else {
                    event.preventDefault();
                    event.stopPropagation();
                    if (this.acceptFileOnDblClick) {
                        const okButton = document.querySelector(`.${BROWSE_FILE_OPEN_CLASS} .jp-mod-accept`);
                        if (okButton) {
                            okButton.click();
                        }
                    }
                }
                break;
            }
            default:
                this.dirListingHandleEvent.call(this.directoryListing, event);
                break;
        }
    }
}
const showBrowseFileDialog = async (manager, options) => {
    const browseFileDialogBody = await BrowseFileDialog.init({
        manager: manager,
        filter: options.filter,
        multiselect: options.multiselect,
        includeDir: options.includeDir,
        rootPath: options.rootPath,
        startPath: options.startPath,
        acceptFileOnDblClick: Object.prototype.hasOwnProperty.call(options, 'acceptFileOnDblClick')
            ? options.acceptFileOnDblClick
            : true
    });
    const dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog({
        title: 'Select a file',
        body: browseFileDialogBody,
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(), _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: 'Select' })]
    });
    dialog.addClass(BROWSE_FILE_CLASS);
    document.body.className += ` ${BROWSE_FILE_OPEN_CLASS}`;
    return dialog.launch().then((result) => {
        document.body.className = document.body.className
            .replace(BROWSE_FILE_OPEN_CLASS, '')
            .trim();
        if (options.rootPath && result.button.accept && result.value.length) {
            const relativeToPath = options.rootPath.endsWith('/')
                ? options.rootPath
                : options.rootPath + '/';
            result.value.forEach((val) => {
                val.path = val.path.replace(relativeToPath, '');
            });
        }
        return result;
    });
};


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   amphiLogo: () => (/* binding */ amphiLogo),
/* harmony export */   asteriskIcon: () => (/* binding */ asteriskIcon),
/* harmony export */   bugIcon: () => (/* binding */ bugIcon),
/* harmony export */   codeIcon: () => (/* binding */ codeIcon),
/* harmony export */   docsIcon: () => (/* binding */ docsIcon),
/* harmony export */   networkIcon: () => (/* binding */ networkIcon),
/* harmony export */   pipelineIcon: () => (/* binding */ pipelineIcon),
/* harmony export */   pipelineNegativeIcon: () => (/* binding */ pipelineNegativeIcon),
/* harmony export */   shieldCheckedIcon: () => (/* binding */ shieldCheckedIcon),
/* harmony export */   squareIcon: () => (/* binding */ squareIcon),
/* harmony export */   uploadIcon: () => (/* binding */ uploadIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_amphi_square_logo_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/amphi-square-logo.svg */ "./style/icons/amphi-square-logo.svg");
/* harmony import */ var _style_icons_amphi_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/icons/amphi.svg */ "./style/icons/amphi.svg");
/* harmony import */ var _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/icons/pipeline-16.svg */ "./style/icons/pipeline-16.svg");
/* harmony import */ var _style_icons_shield_check_24_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/shield-check-24.svg */ "./style/icons/shield-check-24.svg");
/* harmony import */ var _style_icons_code_16_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icons/code-16.svg */ "./style/icons/code-16.svg");
/* harmony import */ var _style_icons_docs_16_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/icons/docs-16.svg */ "./style/icons/docs-16.svg");
/* harmony import */ var _style_icons_upload_16_svg__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/icons/upload-16.svg */ "./style/icons/upload-16.svg");
/* harmony import */ var _style_icons_network_24_svg__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/icons/network-24.svg */ "./style/icons/network-24.svg");
/* harmony import */ var _style_icons_bug_16_svg__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../style/icons/bug-16.svg */ "./style/icons/bug-16.svg");











const asteriskIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:asterisk-icon',
    svgstr: _style_icons_amphi_square_logo_svg__WEBPACK_IMPORTED_MODULE_1__
});
const squareIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:square-icon',
    svgstr: _style_icons_amphi_square_logo_svg__WEBPACK_IMPORTED_MODULE_1__
});
const amphiLogo = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:logo',
    svgstr: _style_icons_amphi_svg__WEBPACK_IMPORTED_MODULE_2__
});
const pipelineIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipeline-icon',
    svgstr: _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_3__
});
const pipelineNegativeIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipelinenegative-icon',
    svgstr: _style_icons_pipeline_16_svg__WEBPACK_IMPORTED_MODULE_3__
});
const shieldCheckedIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:shieldchecked-icon',
    svgstr: _style_icons_shield_check_24_svg__WEBPACK_IMPORTED_MODULE_4__
});
const codeIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:code-icon',
    svgstr: _style_icons_code_16_svg__WEBPACK_IMPORTED_MODULE_5__
});
const docsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:docs-icon',
    svgstr: _style_icons_docs_16_svg__WEBPACK_IMPORTED_MODULE_6__
});
const uploadIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:upload-icon',
    svgstr: _style_icons_upload_16_svg__WEBPACK_IMPORTED_MODULE_7__
});
const networkIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:network-icon',
    svgstr: _style_icons_network_24_svg__WEBPACK_IMPORTED_MODULE_8__
});
const bugIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:bug-icon',
    svgstr: _style_icons_bug_16_svg__WEBPACK_IMPORTED_MODULE_9__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   amphiLogo: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.amphiLogo),
/* harmony export */   asteriskIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.asteriskIcon),
/* harmony export */   bugIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.bugIcon),
/* harmony export */   codeIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.codeIcon),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   docsIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.docsIcon),
/* harmony export */   networkIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.networkIcon),
/* harmony export */   pipelineIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.pipelineIcon),
/* harmony export */   pipelineNegativeIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.pipelineNegativeIcon),
/* harmony export */   shieldCheckedIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.shieldCheckedIcon),
/* harmony export */   showBrowseFileDialog: () => (/* reexport safe */ _BrowseFileDialog__WEBPACK_IMPORTED_MODULE_8__.showBrowseFileDialog),
/* harmony export */   squareIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.squareIcon),
/* harmony export */   uploadIcon: () => (/* reexport safe */ _icons__WEBPACK_IMPORTED_MODULE_10__.uploadIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _launcher__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./launcher */ "./lib/launcher.js");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _BrowseFileDialog__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./BrowseFileDialog */ "./lib/BrowseFileDialog.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");












/**
 * The main application icon.
 */
const logo = {
    id: '@amphi/ui-component:logo',
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, labShell) => {
        let logo = null;
        if (labShell) {
            logo = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget();
            _icons__WEBPACK_IMPORTED_MODULE_10__.asteriskIcon.element({
                container: logo.node,
                elementPosition: 'center',
                margin: '2px 2px 2px 16px',
                height: '16px',
                width: '16px'
            });
        }
        if (logo) {
            logo.id = 'jp-MainLogo';
            app.shell.add(logo, 'top', { rank: 0 });
        }
    }
};
/**
 * The command IDs used by the launcher plugin.
 */
const CommandIDs = {
    create: 'launcher:create'
};
/**
 * The main launcher.
 */
const launcher = {
    id: '@amphi/ui-component:launcher',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_1__.IMainMenu],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.ICommandPalette],
    provides: _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher,
    activate: (app, translator, labShell, mainMenu, manager, palette) => {
        console.log('Amphi - custom Launcher is activated!');
        /** */
        // Use custom Amphi launcher
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const model = new _launcher__WEBPACK_IMPORTED_MODULE_11__.LauncherModel();
        console.log('Amphi - theme before adding launcher:create');
        commands.addCommand(CommandIDs.create, {
            label: trans.__('New'),
            execute: (args) => {
                const cwd = args['cwd'] ? String(args['cwd']) : '';
                const id = `launcher-${Private.id++}`;
                const callback = (item) => {
                    labShell.add(item, 'main', { ref: id });
                };
                const launcher = new _launcher__WEBPACK_IMPORTED_MODULE_11__.Launcher({
                    model,
                    cwd,
                    callback,
                    commands,
                    translator
                }, commands);
                launcher.model = model;
                launcher.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.homeIcon;
                launcher.title.label = trans.__('Homepage');
                const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.MainAreaWidget({ content: launcher });
                // If there are any other widgets open, remove the launcher close icon.
                main.title.closable = !!(0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)(labShell.widgets('main')).length;
                main.id = id;
                shell.add(main, 'main', {
                    activate: args['activate'],
                    ref: args['ref']
                });
                labShell.layoutModified.connect(() => {
                    // If there is only a launcher open, remove the close icon.
                    main.title.closable = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)(labShell.widgets('main')).length > 1;
                }, main);
                return main;
            }
        });
        if (palette) {
            palette.addItem({
                command: CommandIDs.create,
                category: trans.__('Homepage')
            });
        }
        /**
         * This function seems to set up and handle the behavior of an "add" button within a JupyterLab-like environment.
         * When the button is clicked (or an "add" action is requested), the function determines
         * which tab or panel the action was requested from and then executes a command to handle the request,
         * either by creating a main launcher or by performing another default "create" action.
         */
        if (labShell) {
            labShell.addButtonEnabled = true;
            labShell.addRequested.connect((sender, arg) => {
                var _a;
                // Get the ref for the current tab of the tabbar which the add button was clicked
                const ref = ((_a = arg.currentTitle) === null || _a === void 0 ? void 0 : _a.owner.id) ||
                    arg.titles[arg.titles.length - 1].owner.id;
                if (commands.hasCommand('filebrowser:create-main-launcher')) {
                    // If a file browser is defined connect the launcher to it
                    return commands.execute('filebrowser:create-main-launcher', {
                        ref
                    });
                }
                return commands.execute(CommandIDs.create, { ref });
            });
        }
        return model;
    }
};
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The incrementing id used for launcher widgets.
     */
    // eslint-disable-next-line
    Private.id = 0;
})(Private || (Private = {}));
const plugins = [logo, launcher];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);



/***/ }),

/***/ "./lib/launcher.js":
/*!*************************!*\
  !*** ./lib/launcher.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Launcher: () => (/* binding */ Launcher),
/* harmony export */   LauncherModel: () => (/* binding */ LauncherModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/*
 * Copyright 2018-2023 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */




/**
 * The known categories of launcher items and their default ordering.
 */
const AMPHI_CATEGORY = 'Data Integration';
const CommandIDs = {
    newPipeline: 'pipeline-editor:create-new',
    newFile: 'fileeditor:create-new',
    createNewPythonEditor: 'script-editor:create-new-python-editor',
    createNewREditor: 'script-editor:create-new-r-editor'
};
// LauncherModel deals with the underlying data and logic of the launcher (what items are available, their order, etc.).
class LauncherModel extends _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__.LauncherModel {
    /**
     * Return an iterator of launcher items, but remove unnecessary items.
     */
    items() {
        const items = [];
        let pyEditorInstalled = false;
        let rEditorInstalled = false;
        this.itemsList.forEach(item => {
            if (item.command === CommandIDs.createNewPythonEditor) {
                pyEditorInstalled = true;
            }
            else if (item.command === CommandIDs.createNewREditor) {
                rEditorInstalled = true;
            }
        });
        if (!pyEditorInstalled && !rEditorInstalled) {
            return this.itemsList[Symbol.iterator]();
        }
        // Dont add tiles for new py and r files if their script editor is installed
        this.itemsList.forEach(item => {
            var _a, _b;
            if (!(item.command === CommandIDs.newFile &&
                ((pyEditorInstalled && ((_a = item.args) === null || _a === void 0 ? void 0 : _a.fileExt) === 'py') ||
                    (rEditorInstalled && ((_b = item.args) === null || _b === void 0 ? void 0 : _b.fileExt) === 'r')))) {
                items.push(item);
            }
        });
        return items[Symbol.iterator]();
    }
}
// Launcher deals with the visual representation and user interactions of the launcher
// (how items are displayed, icons, categories, etc.).
class Launcher extends _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_0__.Launcher {
    /**
     * Construct a new launcher widget.
     */
    constructor(options, commands) {
        super(options);
        this.myCommands = commands;
        // this._translator = this.translator.load('jupyterlab');
    }
    /**
    The replaceCategoryIcon function takes a category element and a new icon.
    It then goes through the children of the category to find the section header.
    Within the section header, it identifies the icon (by checking if it's not the section title)
    and replaces it with the new icon. The function then returns a cloned version of the original
    category with the icon replaced.
     */
    replaceCategoryIcon(category, icon) {
        const children = react__WEBPACK_IMPORTED_MODULE_2___default().Children.map(category.props.children, child => {
            if (child.props.className === 'jp-Launcher-sectionHeader') {
                const grandchildren = react__WEBPACK_IMPORTED_MODULE_2___default().Children.map(child.props.children, grandchild => {
                    if (grandchild.props.className !== 'jp-Launcher-sectionTitle') {
                        return react__WEBPACK_IMPORTED_MODULE_2___default().createElement(icon.react, { stylesheet: "launcherSection" });
                    }
                    else {
                        return grandchild;
                    }
                });
                return react__WEBPACK_IMPORTED_MODULE_2___default().cloneElement(child, child.props, grandchildren);
            }
            else {
                return child;
            }
        });
        return react__WEBPACK_IMPORTED_MODULE_2___default().cloneElement(category, category.props, children);
    }
    /**
     * Render the launcher to virtual DOM nodes.
     */
    render() {
        // Bail if there is no model.
        if (!this.model) {
            return null;
        }
        // get the rendering from JupyterLab Launcher
        // and resort the categories
        const launcherBody = super.render();
        const launcherContent = launcherBody === null || launcherBody === void 0 ? void 0 : launcherBody.props.children;
        const launcherCategories = launcherContent.props.children;
        const categories = [];
        const knownCategories = [
            AMPHI_CATEGORY,
            //this._translator.__('Console'),
            // this._translator.__('Other'),
            //this._translator.__('Notebook')
        ];
        // Assemble the final ordered list of categories
        // based on knownCategories.
        (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.each)(knownCategories, (category, index) => {
            react__WEBPACK_IMPORTED_MODULE_2___default().Children.forEach(launcherCategories, cat => {
                if (cat.key === category) {
                    if (cat.key === AMPHI_CATEGORY) {
                        cat = this.replaceCategoryIcon(cat, _icons__WEBPACK_IMPORTED_MODULE_3__.pipelineIcon);
                    }
                    categories.push(cat);
                }
            });
        });
        const handleNewPipelineClick = () => {
            console.log("open new pipeline");
            this.myCommands.execute('pipeline-editor:create-new');
        };
        const handleUploadFiles = () => {
            console.log("upload new files");
            this.myCommands.execute('ui-components:file-upload');
        };
        const AlertBox = () => {
            const [isVisible, setIsVisible] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)(false);
            (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
                // Check if the alert was previously closed
                const alertClosed = localStorage.getItem('alertClosed') === 'true';
                setIsVisible(!alertClosed);
            }, []);
            const closeAlert = () => {
                setIsVisible(false);
                // Save the state to prevent the alert from showing again
                localStorage.setItem('alertClosed', 'true');
            };
            if (!isVisible)
                return null;
            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { role: "alert", className: "mt-5 rounded-xl border border-gray-100 bg-white p-4" },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex items-start gap-4" },
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "text-green-600" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("svg", { xmlns: "http://www.w3.org/2000/svg", fill: "none", viewBox: "0 0 24 24", strokeWidth: "1.5", stroke: "currentColor", className: "h-6 w-6" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" }))),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex-1" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h2", { className: "block font-bold text-black-900" }, " Requirements "),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { className: "mt-1 text-sm text-gray-700" }, " Please make sure to use the latest versions of Safari (17+), Google Chrome, or Microsoft Edge. Firefox is not fully supported and you may not be able to run pipelines.")),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("button", { onClick: closeAlert, className: "text-gray-500 transition hover:text-gray-600" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "sr-only" }, "Dismiss popup"),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("svg", { xmlns: "http://www.w3.org/2000/svg", fill: "none", viewBox: "0 0 24 24", strokeWidth: "1.5", stroke: "currentColor", className: "h-6 w-6" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("path", { strokeLinecap: "round", strokeLinejoin: "round", d: "M6 18L18 6M6 6l12 12" }))))));
        };
        // Wrap the sections in body and content divs.
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "jp-Launcher-body" },
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "jp-Launcher-content" },
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h1", { className: "mt-8 text-2xl font-bold text-gray-900 sm:text-3xl flex items-center" },
                    "Amphi ETL",
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "mr-2 ml-2 whitespace-nowrap rounded-full bg-pastel px-2.5 py-0.5 text-sm text-primary" }, "beta")),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement(AlertBox, null),
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "mt-12 grid grid-cols-1 gap-4 lg:grid-cols-3 lg:gap-8" },
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "rounded-lg" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h1", { className: "text-xl font-bold text-gray-900 sm:text-3xl" }, "Start"),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("ul", { className: "mt-4" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", null,
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { onClick: handleNewPipelineClick, className: "flex items-center gap-2 border-s-[3px] border-transparent px-4 py-3 text-primary hover:border-gray-100 hover:bg-gray-50 hover:text-grey-700 cursor-pointer" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.pipelineIcon.react, null),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "text-sm font-medium" }, "New pipeline"))),
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", null,
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: "https://docs.amphi.ai/category/getting-started", className: "flex items-center gap-2 border-s-[3px] border-transparent px-4 py-3 text-grey-500 hover:border-gray-100 hover:bg-gray-50 hover:text-grey-700 cursor-pointer" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.docsIcon.react, null),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "text-sm font-medium" }, "Getting started"))),
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("li", null,
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: "https://join.slack.com/t/amphi-ai/shared_invite/zt-2ci2ptvoy-FENw8AW4ISDXUmz8wcd3bw", className: "flex items-center gap-2 border-s-[3px] border-transparent px-4 py-3 text-grey-500 hover:border-gray-100 hover:bg-gray-50 hover:text-grey-700 cursor-pointer" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.bugIcon.react, null),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "text-sm font-medium" }, "Join the community"))))),
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "rounded-sm lg:col-span-2" },
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h1", { className: "text-xl font-bold text-gray-900 sm:text-3xl" }, "Fundamentals"),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { role: "alert", className: "mt-4 rounded-sm mt-3 border border-gray-100 bg-white p-4" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex items-start gap-4" },
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "text-grey-600" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.codeIcon.react, null)),
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex-1" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h2", { className: "block font-bold text-black-900" }, "Python generation"),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { className: "mt-1 text-sm text-gray-700" }, "Develop data pipelines and generate native Python code you own. Run the pipelines anywhere you'd like.")))),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { role: "alert", className: "mt-4 rounded-xl mt-3 border border-gray-100 bg-white p-4" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex items-start gap-4" },
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "text-grey-600" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.shieldCheckedIcon.react, null)),
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex-1" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h2", { className: "block font-bold text-black-900" }, "Open-source and private"),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { className: "mt-1 text-sm text-gray-700" },
                                        "Amphi ETL is open-source and is self-hosted. All data is stored locally, and isn't sent to or stored on Amphi's servers.",
                                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("a", { href: "https://docs.amphi.ai/getting-started/core-concepts#file-browser", target: "_blank", rel: "noopener noreferrer" }, "Learn more"))))),
                        react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { role: "alert", className: "mt-4 rounded-sm mt-3 border border-gray-100 bg-white p-4" },
                            react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex items-start gap-4" },
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("span", { className: "text-grey-600" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.networkIcon.react, null)),
                                react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: "flex-1" },
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("h2", { className: "block font-bold text-black-900" }, "Community-driven & extensible"),
                                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { className: "mt-1 text-sm text-gray-700" }, "Pipelines can be shared as files with anyone. Coming soon the platform will be extensible with shareable connectors and components.")))))))));
    }
}


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "../../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "../../node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/insertBySelector.js */ "../../node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "../../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "../../node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../../../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "../../node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../node_modules/css-loader/dist/cjs.js!./style/index.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/icons/amphi-square-logo.svg":
/*!*******************************************!*\
  !*** ./style/icons/amphi-square-logo.svg ***!
  \*******************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   width=\"4.000505mm\"\n   height=\"4.0710607mm\"\n   viewBox=\"0 0 4.000505 4.0710607\"\n   version=\"1.1\"\n   id=\"svg1\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   sodipodi:docname=\"amphi-square-logo.svg\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:document-units=\"mm\"\n     inkscape:zoom=\"2.1105281\"\n     inkscape:cx=\"88.603416\"\n     inkscape:cy=\"38.615927\"\n     inkscape:window-width=\"1392\"\n     inkscape:window-height=\"922\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"75\"\n     inkscape:window-maximized=\"0\"\n     inkscape:current-layer=\"layer1\" />\n  <defs\n     id=\"defs1\">\n    <linearGradient\n       id=\"linearGradient14\"\n       inkscape:collect=\"always\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop14\" />\n      <stop\n         style=\"stop-color:#000000;stop-opacity:0;\"\n         offset=\"1\"\n         id=\"stop15\" />\n    </linearGradient>\n    <linearGradient\n       id=\"swatch12\"\n       inkscape:swatch=\"solid\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop13\" />\n    </linearGradient>\n    <rect\n       x=\"123.66742\"\n       y=\"261.60416\"\n       width=\"85.379112\"\n       height=\"35.370846\"\n       id=\"rect1\" />\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient14\"\n       id=\"linearGradient15\"\n       x1=\"124.86797\"\n       y1=\"278.84354\"\n       x2=\"205.72131\"\n       y2=\"278.84354\"\n       gradientUnits=\"userSpaceOnUse\" />\n  </defs>\n  <g\n     inkscape:label=\"Layer 1\"\n     inkscape:groupmode=\"layer\"\n     id=\"layer1\"\n     transform=\"translate(-43.459922,-57.723277)\">\n    <text\n       xml:space=\"preserve\"\n       transform=\"matrix(0.26458333,0,0,0.26458333,10.421939,-14.074989)\"\n       id=\"text1\"\n       style=\"font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:26.6667px;font-family:'Heiti SC';-inkscape-font-specification:'Heiti SC, Normal';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-variant-east-asian:normal;white-space:pre;shape-inside:url(#rect1);display:inline;fill:#5a8f7b;fill-opacity:1;fill-rule:nonzero\"><tspan\n         x=\"123.66797\"\n         y=\"287.87022\"\n         id=\"tspan2\">a</tspan></text>\n  </g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/amphi.svg":
/*!*******************************!*\
  !*** ./style/icons/amphi.svg ***!
  \*******************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n\n<svg\n   width=\"21.392445mm\"\n   height=\"6.6533971mm\"\n   viewBox=\"0 0 21.392445 6.6533971\"\n   version=\"1.1\"\n   id=\"svg1\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   sodipodi:docname=\"amphi.svg\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:document-units=\"mm\"\n     inkscape:zoom=\"6.1387102\"\n     inkscape:cx=\"40.399366\"\n     inkscape:cy=\"10.751444\"\n     inkscape:window-width=\"1312\"\n     inkscape:window-height=\"713\"\n     inkscape:window-x=\"73\"\n     inkscape:window-y=\"186\"\n     inkscape:window-maximized=\"0\"\n     inkscape:current-layer=\"layer1\" />\n  <defs\n     id=\"defs1\">\n    <linearGradient\n       id=\"linearGradient14\"\n       inkscape:collect=\"always\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop14\" />\n      <stop\n         style=\"stop-color:#000000;stop-opacity:0;\"\n         offset=\"1\"\n         id=\"stop15\" />\n    </linearGradient>\n    <linearGradient\n       id=\"swatch12\"\n       inkscape:swatch=\"solid\">\n      <stop\n         style=\"stop-color:#000000;stop-opacity:1;\"\n         offset=\"0\"\n         id=\"stop13\" />\n    </linearGradient>\n    <rect\n       x=\"123.66742\"\n       y=\"261.60416\"\n       width=\"85.379112\"\n       height=\"35.370846\"\n       id=\"rect1\" />\n    <linearGradient\n       inkscape:collect=\"always\"\n       xlink:href=\"#linearGradient14\"\n       id=\"linearGradient15\"\n       x1=\"124.86797\"\n       y1=\"278.84354\"\n       x2=\"205.72131\"\n       y2=\"278.84354\"\n       gradientUnits=\"userSpaceOnUse\" />\n  </defs>\n  <g\n     inkscape:label=\"Layer 1\"\n     inkscape:groupmode=\"layer\"\n     id=\"layer1\"\n     transform=\"translate(-43.459922,-56.375664)\">\n    <text\n       xml:space=\"preserve\"\n       transform=\"matrix(0.26458333,0,0,0.26458333,10.421939,-14.074989)\"\n       id=\"text1\"\n       style=\"font-style:normal;font-variant:normal;font-weight:normal;font-stretch:normal;font-size:26.6667px;font-family:'Heiti SC';-inkscape-font-specification:'Heiti SC, Normal';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-variant-east-asian:normal;white-space:pre;shape-inside:url(#rect1);fill:#5a8f7b;fill-opacity:1;fill-rule:nonzero\"><tspan\n         x=\"123.66797\"\n         y=\"287.87022\"\n         id=\"tspan1\">amphi</tspan></text>\n  </g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/bug-16.svg":
/*!********************************!*\
  !*** ./style/icons/bug-16.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M10.136.803a.75.75 0 011.061 1.06l-.415.416C11.525 2.932 12 3.853 12 4.909c0 .103-.005.205-.014.306.094.016.173.03.238.045a.973.973 0 01.776.951V6.6l1.571-.629a.75.75 0 01.557 1.393L13 8.214v1.13l1.849.246a.75.75 0 11-.198 1.487l-1.659-.221a3.935 3.935 0 01-.426 1.555l2.364.887a.75.75 0 01-.527 1.404l-2.667-1a.752.752 0 01-.12-.058C10.687 14.491 9.384 15 8 15s-2.687-.509-3.616-1.356a.752.752 0 01-.12.058l-2.667 1a.75.75 0 11-.527-1.404l2.364-.887a3.935 3.935 0 01-.426-1.555l-1.659.22a.75.75 0 01-.198-1.486L3 9.343V8.174L.971 7.363a.75.75 0 01.557-1.393L3 6.56V6.21c0-.474.334-.854.776-.95.065-.015.144-.03.238-.046C4.004 5.114 4 5.012 4 4.909c0-1.056.475-1.977 1.218-2.63l-.415-.415A.75.75 0 015.863.803l.695.694a4.318 4.318 0 012.884 0l.694-.694zm-4.63 4.26C6.133 5.026 6.946 5 8 5c1.054 0 1.867.026 2.494.063.004-.051.006-.102.006-.154C10.5 3.793 9.461 2.75 8 2.75S5.5 3.793 5.5 4.91c0 .05.002.102.006.153zM4.5 7.652v-.994C5.043 6.586 6.093 6.5 8 6.5s2.957.086 3.5.158v3.949c0 1.494-1.454 2.893-3.5 2.893-2.046 0-3.5-1.4-3.5-2.893v-.59-2.335-.03z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/code-16.svg":
/*!*********************************!*\
  !*** ./style/icons/code-16.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\"><path d=\"M9.424 2.02a.75.75 0 00-.904.556l-2.5 10.5a.75.75 0 001.46.348l2.5-10.5a.75.75 0 00-.556-.904zM11.2 4.24a.75.75 0 011.06-.04l3.5 3.25a.75.75 0 010 1.1l-3.5 3.25a.75.75 0 11-1.02-1.1L14.148 8 11.24 5.3a.75.75 0 01-.04-1.06zM4.76 5.3a.75.75 0 00-1.02-1.1L.24 7.45a.75.75 0 000 1.1l3.5 3.25a.75.75 0 101.02-1.1L1.852 8 4.76 5.3z\"/></g></svg>";

/***/ }),

/***/ "./style/icons/docs-16.svg":
/*!*********************************!*\
  !*** ./style/icons/docs-16.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M4.25 1A2.25 2.25 0 002 3.25v9.5A2.25 2.25 0 004.25 15h8.5c.69 0 1.25-.56 1.25-1.25V2.25C14 1.56 13.44 1 12.75 1h-8.5zM3.5 12.75c0 .414.336.75.75.75h8.25v-2H4.25a.75.75 0 00-.75.75v.5zm0-2.622c.235-.083.487-.128.75-.128h8.25V2.5H4.25a.75.75 0 00-.75.75v6.878z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/network-24.svg":
/*!************************************!*\
  !*** ./style/icons/network-24.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M10.25 2.5A1.75 1.75 0 008.5 4.25v3.5c0 .966.784 1.75 1.75 1.75H11V11H3a.75.75 0 000 1.5h3.5v2H5.25a1.75 1.75 0 00-1.75 1.75v3.5c0 .966.784 1.75 1.75 1.75h3.5a1.75 1.75 0 001.75-1.75v-3.5a1.75 1.75 0 00-1.75-1.75H8v-2h8v2h-.75a1.75 1.75 0 00-1.75 1.75v3.5c0 .966.784 1.75 1.75 1.75h3.5a1.75 1.75 0 001.75-1.75v-3.5a1.75 1.75 0 00-1.75-1.75H17.5v-2H21a.75.75 0 000-1.5h-8.5V9.5h1.25a1.75 1.75 0 001.75-1.75v-3.5a1.75 1.75 0 00-1.75-1.75h-3.5zM10 4.25a.25.25 0 01.25-.25h3.5a.25.25 0 01.25.25v3.5a.25.25 0 01-.25.25h-3.5a.25.25 0 01-.25-.25v-3.5zm-5 12a.25.25 0 01.25-.25h3.5a.25.25 0 01.25.25v3.5a.25.25 0 01-.25.25h-3.5a.25.25 0 01-.25-.25v-3.5zM15.25 16a.25.25 0 00-.25.25v3.5c0 .138.112.25.25.25h3.5a.25.25 0 00.25-.25v-3.5a.25.25 0 00-.25-.25h-3.5z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/pipeline-16.svg":
/*!*************************************!*\
  !*** ./style/icons/pipeline-16.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M2.75 2.5A1.75 1.75 0 001 4.25v1C1 6.216 1.784 7 2.75 7h1a1.75 1.75 0 001.732-1.5H6.5a.75.75 0 01.75.75v3.5A2.25 2.25 0 009.5 12h1.018c.121.848.85 1.5 1.732 1.5h1A1.75 1.75 0 0015 11.75v-1A1.75 1.75 0 0013.25 9h-1a1.75 1.75 0 00-1.732 1.5H9.5a.75.75 0 01-.75-.75v-3.5A2.25 2.25 0 006.5 4H5.482A1.75 1.75 0 003.75 2.5h-1zM2.5 4.25A.25.25 0 012.75 4h1a.25.25 0 01.25.25v1a.25.25 0 01-.25.25h-1a.25.25 0 01-.25-.25v-1zm9.75 6.25a.25.25 0 00-.25.25v1c0 .138.112.25.25.25h1a.25.25 0 00.25-.25v-1a.25.25 0 00-.25-.25h-1z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/shield-check-24.svg":
/*!*****************************************!*\
  !*** ./style/icons/shield-check-24.svg ***!
  \*****************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><g fill=\"currentColor\"><path d=\"M16.78 8.22a.75.75 0 010 1.06l-5.499 5.5a.75.75 0 01-1.061 0l-2.5-2.5a.75.75 0 111.06-1.06l1.97 1.97 4.97-4.97a.75.75 0 011.06 0z\"/><path fill-rule=\"evenodd\" d=\"M11.04 1.307a2.75 2.75 0 011.92 0l6.25 2.33A2.75 2.75 0 0121 6.214V12c0 2.732-1.462 5.038-3.104 6.774-1.65 1.744-3.562 3-4.65 3.642a2.437 2.437 0 01-2.493 0c-1.087-.643-3-1.898-4.65-3.642C4.463 17.038 3 14.732 3 12V6.214a2.75 2.75 0 011.79-2.577l6.25-2.33zm1.397 1.406a1.25 1.25 0 00-.874 0l-6.25 2.33a1.25 1.25 0 00-.813 1.17V12c0 2.182 1.172 4.136 2.693 5.744 1.514 1.6 3.294 2.772 4.323 3.38.304.18.664.18.968 0 1.03-.608 2.809-1.78 4.323-3.38C18.327 16.136 19.5 14.182 19.5 12V6.214a1.25 1.25 0 00-.813-1.171l-6.25-2.33z\" clip-rule=\"evenodd\"/></g></svg>";

/***/ }),

/***/ "./style/icons/upload-16.svg":
/*!***********************************!*\
  !*** ./style/icons/upload-16.svg ***!
  \***********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\"><path d=\"M4.24 5.8a.75.75 0 001.06-.04l1.95-2.1v6.59a.75.75 0 001.5 0V3.66l1.95 2.1a.75.75 0 101.1-1.02l-3.25-3.5a.75.75 0 00-1.101.001L4.2 4.74a.75.75 0 00.04 1.06z\"/><path d=\"M1.75 9a.75.75 0 01.75.75v3c0 .414.336.75.75.75h9.5a.75.75 0 00.75-.75v-3a.75.75 0 011.5 0v3A2.25 2.25 0 0112.75 15h-9.5A2.25 2.25 0 011 12.75v-3A.75.75 0 011.75 9z\"/></g></svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.3a5d11eaa6df06cb0ee7.js.map