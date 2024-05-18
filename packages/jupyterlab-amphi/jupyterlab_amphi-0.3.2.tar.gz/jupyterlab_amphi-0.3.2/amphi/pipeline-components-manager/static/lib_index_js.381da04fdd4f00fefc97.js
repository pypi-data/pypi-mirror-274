"use strict";
(self["webpackChunk_amphi_pipeline_components_manager"] = self["webpackChunk_amphi_pipeline_components_manager"] || []).push([["lib_index_js"],{

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



const BROWSE_FILE_CLASS = 'amphi-browseFileDialog';
const BROWSE_FILE_OPEN_CLASS = 'amphi-browseFileDialog-open';
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
            const breadcrumbs = document.querySelectorAll('.amphi-browseFileDialog .jp-BreadCrumbs > span[title]');
            breadcrumbs.forEach((crumb) => {
                var _a;
                if (crumb.title.indexOf((_a = this.rootPath) !== null && _a !== void 0 ? _a : '') === 0) {
                    crumb.className = crumb.className
                        .replace('amphi-BreadCrumbs-disabled', '')
                        .trim();
                }
                else if (crumb.className.indexOf('amphi-BreadCrumbs-disabled') === -1) {
                    crumb.className += ' amphi-BreadCrumbs-disabled';
                }
            });
        }
    }
}
/**
 * Browse dialog modal
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

/***/ "./lib/CodeGenerator.js":
/*!******************************!*\
  !*** ./lib/CodeGenerator.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CodeGenerator: () => (/* binding */ CodeGenerator)
/* harmony export */ });
/* harmony import */ var _PipelineService__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./PipelineService */ "./lib/PipelineService.js");
var _a;

class CodeGenerator {
    static generateCode(pipelineJson, commands, componentService) {
        let code = this.generateCodeForNodes(_PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.filterPipeline(pipelineJson), componentService, 'none', true);
        return code;
    }
    static generateCodeUntil(pipelineJson, commands, componentService, targetNode, context) {
        var _b;
        const flow = _PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.filterPipeline(pipelineJson);
        // Only generate code up until target node
        let fromStart = true;
        const previousNodesIds = _PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.findMultiplePreviousNodeIds(flow, targetNode); // list of previous nodes
        const lastExecuted = ((_b = (flow.nodes.find(node => node.id === targetNode) || {}).data) === null || _b === void 0 ? void 0 : _b.lastExecuted) || null;
        const previousLastExecutedValues = flow.nodes
            .filter(node => previousNodesIds.includes(node.id)) // Get lastExecuted from previous nodes
            .map(node => node.data.lastExecuted); // Map to lastExecuted
        const lastUpdatedValues = _PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.getLastUpdatedInPath(flow, targetNode); // Get last updated values
        // Add lastExecuted to the list of previous last executed values
        const allLastExecutedValues = [...previousLastExecutedValues, lastExecuted];
        // Check if any lastUpdated is greater than any of the lastExecuted values
        const updatesSinceLastExecutions = lastUpdatedValues.some(updatedValue => allLastExecutedValues.some(executedValue => updatedValue > executedValue));
        /*
        console.log("updatesSinceLastExecutions %o", updatesSinceLastExecutions)
    
        if(updatesSinceLastExecutions) {
          fromStart = true;
        } else {
          const dataframes = previousNodesIds.map((nodeId) => {
            const nodeCode = this.generateCodeForNodes(flow, componentService, nodeId, false);
            const codeLines = nodeCode.split("\n"); // Split into individual lines
            return codeLines[codeLines.length - 1]; // Get the last line
          });
    
          console.log("Dataframes: %o", dataframes);
      
          dataframes.forEach((df) => {
            const future = context.sessionContext.session.kernel!.requestExecute({ code: "print(_amphi_metadatapanel_getcontentof(" + df + "))" });
            future.onIOPub = msg => {
              if (msg.header.msg_type === 'stream') {
                const streamMsg = msg as KernelMessage.IStreamMsg;
                const output = streamMsg.content.text;
                console.log("output successful")
                fromStart = false;
              } else  {
                const errorMsg = msg as KernelMessage.IErrorMsg;
                const errorOutput = errorMsg.content;
                console.error(`Received error: ${errorOutput.ename}: ${errorOutput.evalue}`);
                fromStart = true;
              }
            };
          });
        }
        */
        if (true) {
            const command = 'pipeline-metadata-panel:delete-all';
            commands.execute(command, {}).catch(reason => {
                console.error(`An error occurred during the execution of ${command}.\n${reason}`);
            });
        }
        const code = this.generateCodeForNodes(flow, componentService, targetNode, true);
        console.log("Code generated %o", code);
        return code;
    }
    static convertToFString(pythonCode) {
        const envVarRegex = /{os\.environ\['(\w+)'\]}/g;
        return pythonCode.replace(/"([^"]*)"/g, (match, group) => {
            let replacedGroup = group;
            let matchResult;
            while ((matchResult = envVarRegex.exec(group)) !== null) {
                const [fullMatch, envVar] = matchResult;
                replacedGroup = replacedGroup.replace(fullMatch, `{os.environ['${envVar}']}`);
            }
            return replacedGroup.includes("{os.environ") ? `f"${replacedGroup}"` : `"${replacedGroup}"`;
        });
    }
}
_a = CodeGenerator;
CodeGenerator.generateCodeForNodes = (flow, componentService, targetNodeId, fromStart) => {
    // Intialization
    let code = '';
    let lastCodeGenerated = '';
    let counters = new Map(); // Map with string as key and integer as value
    const nodesMap = new Map();
    const nodeDependencies = new Map(); // To keep track of node dependencies
    const sortedNodes = []; // To store the topologically sorted nodes
    const loggersMap = new Map();
    const envVariablesMap = new Map();
    const nodeOutputs = new Map();
    const uniqueImports = new Set();
    const uniqueDependencies = new Set();
    const functions = new Set();
    // Helper function to increment counter
    function incrementCounter(key) {
        const count = counters.get(key) || 0;
        counters.set(key, count + 1);
    }
    // Add all pipeline nodes to nodeMap, except annotations and loggers
    flow.nodes.forEach(node => {
        const type = componentService.getComponent(node.type)._type;
        if (type !== 'annotation') {
            if (type === 'logger') {
                loggersMap.set(node.id, node);
            }
            else if (type === 'env_variables') {
                envVariablesMap.set(node.id, node);
            }
            else {
                nodesMap.set(node.id, node);
            }
        }
    });
    // Topological sort with path tracking
    const visited = new Set();
    const nodePaths = new Map();
    const topologicalSortWithPathTracking = (node, path) => {
        if (visited.has(node)) {
            // Combine the current path with the existing path for the node
            const existingPath = nodePaths.get(node) || new Set();
            nodePaths.set(node, new Set([...existingPath, ...path]));
            return;
        }
        visited.add(node);
        const dependencies = flow.edges
            .filter(edge => edge.target === node)
            .map(edge => edge.source);
        nodeDependencies.set(node, dependencies);
        // Include the current node in the path for subsequent calls
        const currentPath = new Set([...path, node]);
        nodePaths.set(node, currentPath);
        dependencies.forEach(dependency => {
            topologicalSortWithPathTracking(dependency, currentPath);
        });
        sortedNodes.push(node);
    };
    // Perform topological sort with path tracking
    flow.nodes.forEach(node => {
        if (!visited.has(node.id)) {
            topologicalSortWithPathTracking(node.id, new Set());
        }
    });
    // Assume sortedNodes is already populated from the topological sort
    let nodesToTraverse = [];
    // After topological sorting and path tracking
    if (targetNodeId !== 'none') {
        let nodesToConsider = new Set([targetNodeId]);
        let pathToTarget = new Set();
        while (nodesToConsider.size > 0) {
            let nextNodesToConsider = new Set();
            nodesToConsider.forEach(nodeId => {
                pathToTarget.add(nodeId);
                const dependencies = nodeDependencies.get(nodeId) || [];
                dependencies.forEach(dep => {
                    if (!pathToTarget.has(dep)) {
                        nextNodesToConsider.add(dep);
                    }
                });
            });
            nodesToConsider = nextNodesToConsider;
        }
        // Filter the sortedNodes to include only those in pathToTarget, preserving the topological order
        nodesToTraverse = sortedNodes.filter(nodeId => pathToTarget.has(nodeId));
    }
    else {
        nodesToTraverse = sortedNodes;
    }
    // nodesToTraverse.reverse();
    for (const nodeId of nodesToTraverse) {
        const node = nodesMap.get(nodeId);
        if (!node) {
            console.error(`Node with id ${nodeId} not found.`);
            continue;
        }
        let config = node.data; // Initialize config
        const component = componentService.getComponent(node.type);
        const component_type = componentService.getComponent(node.type)._type;
        const component_id = componentService.getComponent(node.type)._id;
        // Only gather additionnal dependencies if the function exists
        if (typeof (component === null || component === void 0 ? void 0 : component.provideDependencies) === 'function') {
            const deps = component.provideDependencies({ config });
            deps.forEach(dep => uniqueDependencies.add(dep));
        }
        const imports = component.provideImports({ config }); // Gather imports
        imports.forEach(importStatement => uniqueImports.add(importStatement));
        // Gather functions
        if (typeof (component === null || component === void 0 ? void 0 : component.provideFunctions) === 'function') {
            component.provideFunctions({ config }).forEach(func => functions.add(func));
        }
        // Initiliaze input and output variables
        let inputName = '';
        let outputName = '';
        switch (component_type) {
            case 'pandas_df_processor':
                incrementCounter(component_id);
                inputName = nodeOutputs.get(_PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.findPreviousNodeId(flow, nodeId));
                outputName = `${node.type}${counters.get(component_id)}`;
                nodeOutputs.set(nodeId, outputName); // Map the source node to its output variable
                lastCodeGenerated = componentService.getComponent(node.type).generateComponentCode({ config, inputName, outputName });
                break;
            case 'pandas_df_double_processor':
                const [input1Id, input2Id] = _PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.findMultiplePreviousNodeIds(flow, nodeId);
                incrementCounter(component_id);
                outputName = `${node.type}${counters.get(component_id)}`;
                nodeOutputs.set(node.id, outputName);
                const inputName1 = nodeOutputs.get(input1Id);
                const inputName2 = nodeOutputs.get(input2Id);
                lastCodeGenerated = componentService.getComponent(node.type).generateComponentCode({
                    config,
                    inputName1,
                    inputName2,
                    outputName
                });
                break;
            case 'pandas_df_input':
                incrementCounter(component_id);
                outputName = `${node.type}${counters.get(component_id)}`;
                nodeOutputs.set(nodeId, outputName); // Map the source node to its output variable
                lastCodeGenerated = componentService.getComponent(node.type).generateComponentCode({ config, outputName });
                break;
            case 'pandas_df_output':
                incrementCounter(component_id);
                inputName = nodeOutputs.get(_PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.findPreviousNodeId(flow, nodeId));
                lastCodeGenerated = componentService.getComponent(node.type).generateComponentCode({ config, inputName });
                break;
            default:
                console.error("Error generating code.");
        }
        code += lastCodeGenerated;
        // If target node....  
        if (nodeId === targetNodeId) {
            if (component_type.includes('processor') || component_type.includes('input')) {
                if (!fromStart) {
                    code = lastCodeGenerated;
                }
                code += '\n' + nodeOutputs.get(nodeId);
            }
            else if (component_type.includes('output')) {
                // Add try block and indent existing code
                const indentedCode = code.split('\n').map(line => '    ' + line).join('\n');
                code = 'try:\n' + indentedCode + '\n    print("Pipeline Execution: SUCCESS")\n';
                code += 'except Exception as e:\n';
                code += '    print(f"Pipeline Execution: FAILED with error {e}")\n';
                code += '    raise\n'; // Re-raise the exception to propagate the error status
            }
        }
    }
    let envVariablesCode = '';
    // Loggers when full pipeline execution
    if (envVariablesMap.size > 0) {
        envVariablesMap.forEach((node, nodeId) => {
            // Process each logger
            const component = componentService.getComponent(node.type);
            let config = node.data; // Initialize config
            const imports = component.provideImports({ config }); // Gather imports
            imports.forEach(importStatement => uniqueImports.add(importStatement));
            envVariablesCode += componentService.getComponent(node.type).generateComponentCode({ config });
        });
    }
    else {
        console.log('No env variables component found.');
    }
    // Loggers when full pipeline execution
    if (loggersMap.size > 0) {
        let loggerCode = '';
        loggersMap.forEach((node, nodeId) => {
            // Process each logger
            const component = componentService.getComponent(node.type);
            let config = node.data; // Initialize config
            // Only gather additionnal dependencies if the function exists
            if (typeof (component === null || component === void 0 ? void 0 : component.provideDependencies) === 'function') {
                const deps = component.provideDependencies({ config });
                deps.forEach(dep => uniqueDependencies.add(dep));
            }
            if (typeof (component === null || component === void 0 ? void 0 : component.provideFunctions) === 'function') {
                component.provideFunctions({ config }).forEach(func => functions.add(func));
            }
            const imports = component.provideImports({ config }); // Gather imports
            imports.forEach(importStatement => uniqueImports.add(importStatement));
            loggerCode += componentService.getComponent(node.type).generateComponentCode({ config });
        });
        // Indentation for the Python code block
        const indent = '    ';
        loggerCode = loggerCode.split('\n').map(line => indent + line).join('\n');
        code = code.split('\n').map(line => indent + line).join('\n');
        code = `
try:
${code}
except Exception as e:
    print(f"An error occurred: {e}")
${loggerCode}
`;
    }
    else {
        // console.log('No loggers found.');
    }
    const currentDate = new Date();
    const dateString = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getDate().toString().padStart(2, '0')} ${currentDate.getHours().toString().padStart(2, '0')}:${currentDate.getMinutes().toString().padStart(2, '0')}:${currentDate.getSeconds().toString().padStart(2, '0')}`;
    const dateComment = `# Source code generated by Amphi\n# Date: ${dateString}`;
    const additionalImports = `# Additional dependencies: ${Array.from(uniqueDependencies).join(', ')}`;
    // Replace variabale string 
    code = _a.convertToFString(code);
    const generatedCode = `${dateComment}
${additionalImports}
${Array.from(uniqueImports).join('\n')}
\n${envVariablesCode}${Array.from(functions).join('\n\n')}
${code}`;
    return generatedCode;
};
;


/***/ }),

/***/ "./lib/DndProviderWrapper.js":
/*!***********************************!*\
  !*** ./lib/DndProviderWrapper.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dnd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dnd */ "webpack/sharing/consume/default/react-dnd/react-dnd");
/* harmony import */ var react_dnd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dnd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_dnd_html5_backend__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-dnd-html5-backend */ "webpack/sharing/consume/default/react-dnd-html5-backend/react-dnd-html5-backend");
/* harmony import */ var react_dnd_html5_backend__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_dnd_html5_backend__WEBPACK_IMPORTED_MODULE_2__);
// DndProviderWrapper.tsx



const DndProviderWrapper = ({ children }) => {
    const context = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [dndArea, setDnDArea] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(context.current);
    const updateDndArea = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(() => {
        setDnDArea(context === null || context === void 0 ? void 0 : context.current);
    }, []);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        updateDndArea();
    }, [updateDndArea]);
    const html5Options = (0,react__WEBPACK_IMPORTED_MODULE_0__.useMemo)(() => ({ rootElement: dndArea }), [dndArea]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { ref: context }, dndArea && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_dnd__WEBPACK_IMPORTED_MODULE_1__.DndProvider, { backend: react_dnd_html5_backend__WEBPACK_IMPORTED_MODULE_2__.HTML5Backend, options: html5Options }, children))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DndProviderWrapper);


/***/ }),

/***/ "./lib/PipelineComponent.js":
/*!**********************************!*\
  !*** ./lib/PipelineComponent.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PipelineComponent: () => (/* binding */ PipelineComponent)
/* harmony export */ });
function PipelineComponent() {
    return class {
        constructor() { }
        static getInstance() {
            if (!this.instance) {
                this.instance = new this();
            }
            return this.instance;
        }
        static get Name() {
            const instance = this.getInstance();
            return instance._name;
        }
        static get Type() {
            const instance = this.getInstance();
            return instance._type;
        }
        // Static getter for the icon
        static get Icon() {
            const instance = this.getInstance();
            return instance._icon;
        }
        // Static getter for the default config
        static get Default() {
            const instance = this.getInstance();
            return instance._default;
        }
        // Static getter for the default config
        static get Form() {
            const instance = this.getInstance();
            return instance._form;
        }
    };
}


/***/ }),

/***/ "./lib/PipelineService.js":
/*!********************************!*\
  !*** ./lib/PipelineService.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   PipelineService: () => (/* binding */ PipelineService)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);

class PipelineService {
    static filterPipeline(pipelineJson) {
        const pipeline = JSON.parse(pipelineJson);
        const pipelineFlow = pipeline.pipelines[0].flow;
        const filteredNodes = pipelineFlow.nodes.map(({ id, type, data }) => ({ id, type, data }));
        const filteredEdges = pipelineFlow.edges.map(({ id, source, target, targetHandle }) => ({ id, source, target, targetHandle }));
        const flow = {
            "nodes": filteredNodes,
            "edges": filteredEdges
        };
        return flow;
    }
    // Function to retrieve the names of packages
    static extractPackageNames(imports) {
        const standardLibraries = new Set(['json', 'pandas']);
        return imports.map((imp) => {
            let packageName = "";
            if (imp.startsWith("import ")) {
                packageName = imp.split(" ")[1].split(" as ")[0]; // For "import packageName" format
            }
            else if (imp.startsWith("from ")) {
                packageName = imp.split(" ")[1]; // For "from packageName import something" format
            }
            else {
                packageName = imp; // Assuming direct package name
            }
            if (!standardLibraries.has(packageName)) {
                return packageName;
            }
            return ""; // Return an empty string for packages in the standardLibraries set
        }).filter((pkgName, index, self) => pkgName && self.indexOf(pkgName) === index); // Removing empty strings, duplicates
    }
    // Function to generate pip install commands from a list of package names
    static getInstallCommandsFromPackageNames(packageNames) {
        return packageNames.map(pkgName => `!pip install ${pkgName} -q -q`);
    }
    static extractPythonImportPackages(code) {
        // Regular expression to match Python import statements
        const importRegex = /^(import .+|from .+? import .+)/gm;
        let matches = code.match(importRegex) || [];
        // Process each match to format correctly
        return matches.map((importStatement) => {
            if (importStatement.startsWith('from')) {
                // If the statement starts with 'from', extract the package part before the first dot
                return importStatement.split(' ')[1].split('.')[0];
            }
            else {
                // Otherwise, it's a regular import, extract everything after 'import '
                return importStatement.split(' ')[1];
            }
        });
    }
    /**
     * Check if a given file is allowed to be added to the pipeline
     * @param item
     */
    static getPipelineRelativeNodePath(pipelinePath, nodePath) {
        const relativePath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.relative(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.dirname(pipelinePath), nodePath);
        return relativePath;
    }
    static getComponentIdForFileExtension(item, componentService) {
        // Extract file extension from item.name
        const fileExtension = item.name.split('.').pop();
        if (!fileExtension)
            return { id: null, default: null }; // Return nulls if there is no file extension
        // Retrieve all components
        const components = componentService.getComponents();
        // Iterate through all components
        for (const component of components) {
            // Check if the component has the _fileDrop attribute and it contains the file extension
            if (component._fileDrop && component._fileDrop.includes(fileExtension.toLowerCase())) {
                // Return the component's _id and _default if the file extension matches
                return { id: component._id, default: component._default || null };
            }
        }
        return { id: null, default: null }; // Return nulls if no matching component is found
    }
    static getLastUpdatedInPath(flow, targetId) {
        const visited = new Set();
        const lastUpdatedList = [];
        const findNodesInPath = (nodeId) => {
            if (visited.has(nodeId)) {
                return;
            }
            visited.add(nodeId);
            const node = flow.nodes.find(n => n.id === nodeId);
            if (node && node.data && node.data.lastUpdated) {
                lastUpdatedList.push(node.data.lastUpdated);
            }
            const dependencies = flow.edges
                .filter(edge => edge.target === nodeId)
                .map(edge => edge.source);
            dependencies.forEach(dependency => {
                findNodesInPath(dependency);
            });
        };
        findNodesInPath(targetId);
        return lastUpdatedList;
    }
    static getEnvironmentVariables(pipelineJson) {
        const flow = PipelineService.filterPipeline(pipelineJson);
        const envVariablesNodes = flow.nodes.filter(node => node.type === 'envVariables');
        const variablesList = envVariablesNodes.reduce((acc, node) => {
            return acc.concat(node.data.variables || []);
        }, []);
        return variablesList;
    }
}
PipelineService.findStartNode = (flow, componentService) => {
    const targetMap = new Set();
    flow.edges.forEach(edge => targetMap.add(edge.target));
    for (const node of flow.nodes) {
        const nodeType = componentService.getComponent(node.type)._type;
        if (!targetMap.has(node.id) && nodeType === "pandas_df_input") {
            return node.id;
        }
    }
    return null;
};
PipelineService.findStartNodes = (flow, componentService) => {
    const targetMap = new Set();
    flow.edges.forEach(edge => targetMap.add(edge.target));
    const startNodes = [];
    for (const node of flow.nodes) {
        const nodeType = componentService.getComponent(node.type)._type;
        if (!targetMap.has(node.id) && nodeType === "pandas_df_input") {
            startNodes.push(node.id);
            if (startNodes.length === 2) {
                // If we've found two start nodes, assume it's the double processor case
                return startNodes;
            }
        }
    }
    if (startNodes.length === 1) {
        // If there's only one start node, return it as an array
        return startNodes;
    }
    // If no start nodes are found, return an empty array
    return [];
};
PipelineService.findPreviousNodeId = (flow, nodeId) => {
    // Find the ID of the previous node
    let previousNodeId = '';
    flow.edges.forEach(edge => {
        if (edge.target === nodeId) {
            previousNodeId = edge.source;
        }
    });
    return previousNodeId;
};
PipelineService.findMultiplePreviousNodeIds = (flow, nodeId) => {
    const previousNodesMap = new Map();
    // Group incoming edges by targetHandle
    flow.edges.forEach(edge => {
        if (edge.target === nodeId) {
            const handle = edge.targetHandle || 'default'; // Fallback to 'default' if no handle
            if (!previousNodesMap.has(handle)) {
                previousNodesMap.set(handle, []);
            }
            previousNodesMap.get(handle).push(edge.source);
        }
    });
    // Sort the map by targetHandle and flatten the result
    const sortedPreviousNodeIds = Array.from(previousNodesMap.entries())
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(([_, nodeIds]) => nodeIds)
        .reduce((acc, val) => acc.concat(val), []);
    return sortedPreviousNodeIds;
};
PipelineService.findTwoPreviousNodeIds = (flow, nodeId) => {
    let previousNodeIds = [];
    flow.edges.forEach(edge => {
        if (edge.target === nodeId) {
            previousNodeIds.push(edge.source);
        }
    });
    if (previousNodeIds.length !== 2) {
        throw new Error("Exactly two previous nodes are not found.");
    }
    return previousNodeIds;
};


/***/ }),

/***/ "./lib/RequestService.js":
/*!*******************************!*\
  !*** ./lib/RequestService.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RequestService: () => (/* binding */ RequestService)
/* harmony export */ });
/* harmony import */ var _CodeGenerator__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./CodeGenerator */ "./lib/CodeGenerator.js");
/* harmony import */ var _PipelineService__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./PipelineService */ "./lib/PipelineService.js");


class RequestService {
    static retrieveDataframeColumns(event, context, commands, componentService, setItems, setLoadings, nodeId, inputNb, previousNodes) {
        setLoadings(true);
        const flow = _PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.filterPipeline(context.model.toString());
        let code = '';
        try {
            let refNodeId = previousNodes ? _PipelineService__WEBPACK_IMPORTED_MODULE_0__.PipelineService.findMultiplePreviousNodeIds(flow, nodeId)[inputNb] : nodeId;
            code = _CodeGenerator__WEBPACK_IMPORTED_MODULE_1__.CodeGenerator.generateCodeUntil(context.model.toString(), commands, componentService, refNodeId, context);
        }
        catch (error) {
            console.error("Error generating code.", error);
            code = null; // Or handle error appropriately
            setLoadings(false);
        }
        const lines = code.split('\n');
        const output_df = lines.pop(); // Extract the last line and store it in output_df
        if (output_df && output_df.trim() && output_df.trim().split(' ').length === 1) {
            code = lines.join('\n'); // Rejoin the remaining lines back into code
            const future = context.sessionContext.session.kernel.requestExecute({ code: code });
            future.onReply = reply => {
                if (reply.content.status == "ok") {
                    const future2 = context.sessionContext.session.kernel.requestExecute({ code: "print(_amphi_metadatapanel_getcontentof(" + output_df + "))" });
                    future2.onIOPub = msg => {
                        if (msg.header.msg_type === 'stream') {
                            const streamMsg = msg;
                            const output = streamMsg.content.text;
                            const regex = /([^,]+)\s+\(([^,]+),\s*(named|unnamed)\)/g;
                            const newItems = [];
                            let match;
                            while ((match = regex.exec(output)) !== null) {
                                const [_, name, type, namedStatus] = match;
                                newItems.push({
                                    value: name.trim(),
                                    label: name.trim(),
                                    type: type.trim(),
                                    named: namedStatus.trim() === 'named' // true if 'named', false if 'unnamed'
                                });
                            }
                            console.log("Retrieve col, new items %o", newItems);
                            // Update the items array with the new items, ensuring no duplicates
                            setItems(items => {
                                const itemSet = new Set(items.map(item => item.value)); // Create a set of existing item values
                                const uniqueItems = newItems.filter(newItem => !itemSet.has(newItem.value));
                                console.log("Retrieve col, uniqueItems %o", uniqueItems);
                                return [...items, ...uniqueItems];
                            });
                            setLoadings(false);
                        }
                        else if (msg.header.msg_type === 'error') {
                            setLoadings(false);
                            const errorMsg = msg;
                            const errorOutput = errorMsg.content;
                            console.error(`Received error: ${errorOutput.ename}: ${errorOutput.evalue}`);
                        }
                    };
                }
                else if (reply.content.status == "error") {
                    setLoadings(false);
                }
                else if (reply.content.status == "abort") {
                    setLoadings(false);
                }
                else {
                    setLoadings(false);
                }
            };
        }
        else {
            setLoadings(false);
        }
    }
    ;
    static retrieveTableColumns(event, connectionString, tableName, query, context, commands, componentService, setDataSource, setLoadings, nodeId) {
        setLoadings(true);
        const code = `
!pip install --quiet pymysql --disable-pip-version-check
import pandas as pd
from sqlalchemy import create_engine
schema = pd.read_sql("${query}", con = create_engine("${connectionString}"))
column_info = schema[["Field", "Type"]]
formatted_output = ", ".join([f"{row['Field']} ({row['Type']})" for _, row in column_info.iterrows()])
print(formatted_output)
`;
        console.log("code: " + code);
        const future = context.sessionContext.session.kernel.requestExecute({ code: code });
        future.onReply = reply => {
            if (reply.content.status == "ok") {
                console.log("OK");
            }
            else if (reply.content.status == "error") {
                console.log("error");
                setLoadings(false);
            }
            else if (reply.content.status == "abort") {
                console.log("abort");
                setLoadings(false);
            }
            else {
                console.log("Other");
                setLoadings(false);
            }
        };
        future.onIOPub = msg => {
            if (msg.header.msg_type === 'stream') {
                const streamMsg = msg;
                const output = streamMsg.content.text;
                const regex = /([^\s,]+)\s+\(((?:[^()]+|\([^)]*\))*)\)/g;
                const newItems = [];
                let match;
                while ((match = regex.exec(output)) !== null) {
                    const [_, name, type, namedStatus] = match;
                    newItems.push({
                        input: {},
                        value: name,
                        key: name,
                        type: type.toUpperCase()
                    });
                }
                setDataSource((items) => {
                    // Create a set of existing item keys
                    const existingKeys = new Set(items.map((item) => item.key));
                    // Filter newItems to ensure unique keys
                    const uniqueItems = newItems.filter((newItem) => !existingKeys.has(newItem.key));
                    return [...items, ...uniqueItems];
                });
                setLoadings(false);
            }
            else if (msg.header.msg_type === 'error') {
                setLoadings(false);
                const errorMsg = msg;
                const errorOutput = errorMsg.content;
                console.error(`Received error: ${errorOutput.ename}: ${errorOutput.evalue}`);
            }
        };
    }
    ;
}


/***/ }),

/***/ "./lib/configUtils.js":
/*!****************************!*\
  !*** ./lib/configUtils.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ ConfigModal),
/* harmony export */   generateUIFormComponent: () => (/* binding */ generateUIFormComponent),
/* harmony export */   generateUIInputs: () => (/* binding */ generateUIInputs),
/* harmony export */   onChange: () => (/* binding */ onChange),
/* harmony export */   setDefaultConfig: () => (/* binding */ setDefaultConfig)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/SearchOutlined.js");
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/CheckOutlined.js");
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/CloseOutlined.js");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _BrowseFileDialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./BrowseFileDialog */ "./lib/BrowseFileDialog.js");
/* harmony import */ var _forms_keyValueForm__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./forms/keyValueForm */ "./lib/forms/keyValueForm.js");
/* harmony import */ var _forms_valuesListForm__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./forms/valuesListForm */ "./lib/forms/valuesListForm.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _forms_InputRegular__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./forms/InputRegular */ "./lib/forms/InputRegular.js");
/* harmony import */ var _forms_selectCustomizable__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./forms/selectCustomizable */ "./lib/forms/selectCustomizable.js");
/* harmony import */ var _forms_selectTokenization__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./forms/selectTokenization */ "./lib/forms/selectTokenization.js");
/* harmony import */ var _forms_selectRegular__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./forms/selectRegular */ "./lib/forms/selectRegular.js");
/* harmony import */ var _forms_selectColumns__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./forms/selectColumns */ "./lib/forms/selectColumns.js");
/* harmony import */ var _forms_selectColumn__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./forms/selectColumn */ "./lib/forms/selectColumn.js");
/* harmony import */ var _forms_keyValueColumns__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./forms/keyValueColumns */ "./lib/forms/keyValueColumns.js");
/* harmony import */ var _forms_keyValueColumnsSelect__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./forms/keyValueColumnsSelect */ "./lib/forms/keyValueColumnsSelect.js");
/* harmony import */ var _forms_transferData__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./forms/transferData */ "./lib/forms/transferData.js");
/* harmony import */ var _forms_TextareaRegular__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./forms/TextareaRegular */ "./lib/forms/TextareaRegular.js");
/* harmony import */ var _forms_dataMapping__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./forms/dataMapping */ "./lib/forms/dataMapping.js");
/* harmony import */ var _forms_CodeTextarea__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./forms/CodeTextarea */ "./lib/forms/CodeTextarea.js");




















const setDefaultConfig = ({ nodeId, store, setNodes, defaultConfig, }) => {
    const { nodeInternals } = store.getState();
    setNodes(Array.from(nodeInternals.values()).map((node) => {
        if (node.id === nodeId && Object.keys(node.data).length === 1) {
            node.data = {
                ...defaultConfig,
                lastUpdated: null,
                lastExecuted: null,
            };
        }
        return node;
    }));
};
const onChange = ({ evtTargetValue, field, nodeId, store, setNodes }) => {
    const newValue = evtTargetValue;
    const { nodeInternals } = store.getState();
    const currentTimestamp = Date.now(); // Current timestamp in milliseconds since Unix epoch
    setNodes(Array.from(nodeInternals.values()).map((node) => {
        if (node.id === nodeId) {
            let fieldParts = field.split('.');
            // Set or update the main field
            if (fieldParts.length === 1) {
                // Top-level field
                node.data = { ...node.data, [field]: newValue };
            }
            else {
                // Nested field
                const [outerField, innerField] = fieldParts;
                node.data = {
                    ...node.data,
                    [outerField]: {
                        ...node.data[outerField],
                        [innerField]: newValue,
                    },
                };
            }
            // Set or update the lastUpdated field with the current timestamp
            if (field !== 'lastExecuted') {
                node.data = { ...node.data, lastUpdated: currentTimestamp };
            }
            else {
                node.data = { ...node.data };
            }
        }
        return node;
    }));
};
const generateUIFormComponent = ({ nodeId, type, name, form, data, context, componentService, manager, commands, handleChange, }) => {
    const [modalOpen, setModalOpen] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const executeUntilComponent = () => {
        commands.execute('pipeline-editor:run-pipeline-until', { nodeId: nodeId, context: context });
        handleChange(Date.now(), 'lastExecuted');
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.ConfigProvider, { theme: {
            token: {
                // Seed Token
                colorPrimary: '#5F9B97',
            },
        } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form, { layout: "vertical", size: "small" },
            generateUIInputs({ name, nodeId, form, data, context, componentService, manager, commands, handleChange, advanced: false }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "flex justify-center mt-1 pt-1.5 space-x-4" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { onClick: () => setModalOpen(true), className: "inline-flex items-center justify-center cursor-pointer group" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.settingsIcon.react, { className: "h-3 w-3 group-hover:text-primary" })),
                (type.includes('input') || type.includes('processor') || type.includes('output')) && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { onClick: executeUntilComponent, className: "inline-flex items-center justify-center cursor-pointer group" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_3__.playCircleIcon.react, { className: "h-3 w-3 group-hover:text-primary" })))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(ConfigModal, { modalOpen: modalOpen, setModalOpen: setModalOpen, name: name, nodeId: nodeId, form: form, data: data, context: context, componentService: componentService, manager: manager, commands: commands, handleChange: handleChange, advanced: true }))));
};
const generateUIInputs = ({ name, nodeId, form, data, context, componentService, manager, commands, handleChange, advanced }) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null, form.fields.map((field, index) => {
        if (!advanced && field.advanced) {
            return null;
        }
        // if unique value
        let value;
        // if list
        let values = [];
        const fieldParts = field.id.split('.');
        if (Array.isArray(data[field.id])) {
            // We're dealing with a list item
            values = data[field.id];
        }
        else if (fieldParts.length === 1) {
            // Top-level field
            if (data[field.id] !== undefined) {
                value = data[field.id];
            }
        }
        else {
            // Nested field
            const [outerField, innerField] = fieldParts;
            if (data[outerField] && data[outerField][innerField] !== undefined) {
                value = data[outerField][innerField];
            }
        }
        const validateInput = (value) => {
            if (field.validation) { // Check if field.validation exists
                const pattern = new RegExp(field.validation, "i"); // Creates the regex
                setIsInvalid(!pattern.test(value));
            }
            else {
                setIsInvalid(false); // If no field.validation, consider the input as valid
            }
        };
        const [isInvalid, setIsInvalid] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
        // Use useEffect to call validateInput whenever 'value' changes
        (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
            validateInput(value);
        }, [value]); // Dependency array ensures this effect runs whenever 'value' changes
        switch (field.type) {
            case "input":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { style: { marginTop: "5px", padding: "0 0 2px" }, label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_InputRegular__WEBPACK_IMPORTED_MODULE_4__["default"], { field: field, value: value, handleChange: handleChange, context: context, advanced: advanced })));
            case "radio":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Flex, { vertical: true, gap: "middle" },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Radio.Group, { defaultValue: value, onChange: (e) => handleChange(e.target.value, field.id), buttonStyle: "solid" }, field.options.map(option => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Radio.Button, { value: option.value }, option.label)))))));
            case "file":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { style: { marginTop: "5px", padding: "0 0 2px" }, label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space.Compact, { style: { width: '100%' } },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { id: field.id, size: advanced ? "middle" : "small", name: field.id, placeholder: field.placeholder, onChange: (e) => handleChange(e.target.value, field.id), value: value, ...(isInvalid ? { status: "warning" } : {}) }),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "primary", size: advanced ? "middle" : "small", onClick: async () => {
                                // TODO, there is something wrong here
                                const workspacePath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.resolve('/', _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.dirname(context.path));
                                const res = await (0,_BrowseFileDialog__WEBPACK_IMPORTED_MODULE_5__.showBrowseFileDialog)(manager, {
                                    multiselect: false,
                                    includeDir: true,
                                    rootPath: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.dirname(context.path),
                                    filter: (model) => {
                                        return model.path !== context.path;
                                    }
                                });
                                handleChange(res.value[0].path, field.id);
                            } },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_6__["default"], null)))));
            case "columns":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { style: { marginTop: "5px", padding: "0 0 2px" }, label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_selectColumns__WEBPACK_IMPORTED_MODULE_7__["default"], { field: field, handleChange: handleChange, defaultValues: values, context: context, componentService: componentService, commands: commands, nodeId: nodeId, inDialog: advanced })));
            case "column":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { style: { marginTop: "5px", padding: "0 0 2px" }, label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_selectColumn__WEBPACK_IMPORTED_MODULE_8__["default"], { field: field, handleChange: handleChange, defaultValue: value, context: context, componentService: componentService, commands: commands, nodeId: nodeId, inDialog: advanced })));
            case "selectCustomizable":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_selectCustomizable__WEBPACK_IMPORTED_MODULE_9__["default"], { field: field, handleChange: handleChange, defaultValue: value, inDialog: advanced })));
            case "selectTokenization":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_selectTokenization__WEBPACK_IMPORTED_MODULE_10__["default"], { field: field, handleChange: handleChange, defaultValue: value, inDialog: advanced })));
            case "select":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_selectRegular__WEBPACK_IMPORTED_MODULE_11__["default"], { field: field, handleChange: handleChange, defaultValue: value, inDialog: advanced })));
            case "textarea":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_TextareaRegular__WEBPACK_IMPORTED_MODULE_12__["default"], { field: field, value: value, handleChange: handleChange, advanced: advanced, rows: field.rows })));
            case "codeTextarea":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_CodeTextarea__WEBPACK_IMPORTED_MODULE_13__["default"], { field: field, value: value, handleChange: handleChange, advanced: advanced, rows: field.rows })));
            case "boolean":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { style: { marginTop: "5px", padding: "0 0 2px" }, label: field.label, ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Switch, { onChange: (checked) => handleChange(checked, field.id), checkedChildren: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_14__["default"], null), unCheckedChildren: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_15__["default"], null), defaultChecked: value === true })));
            case "cascader":
                const displayRender = (labels) => labels[labels.length - 1];
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Cascader, { value: values, placeholder: field.placeholder, options: field.options, displayRender: displayRender, onChange: (value) => handleChange(value, field.id) })));
            case "keyvalue":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_keyValueForm__WEBPACK_IMPORTED_MODULE_16__.KeyValueForm, { field: field, handleChange: handleChange, initialValues: values })));
            case "keyvalueColumns":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_keyValueColumns__WEBPACK_IMPORTED_MODULE_17__["default"], { field: field, handleChange: handleChange, initialValues: values, context: context, componentService: componentService, commands: commands, nodeId: nodeId, inDialog: advanced })));
            case "keyvalueColumnsSelect":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_keyValueColumnsSelect__WEBPACK_IMPORTED_MODULE_18__["default"], { field: field, handleChange: handleChange, initialValues: values, context: context, componentService: componentService, commands: commands, nodeId: nodeId, inDialog: advanced })));
            case "valuesList":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_valuesListForm__WEBPACK_IMPORTED_MODULE_19__.ValuesListForm, { field: field, handleChange: handleChange, initialValues: values })));
            case "inputNumber":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, className: "nodrag", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.InputNumber, { ...(field.min ? { min: field.min } : {}), ...(field.max ? { max: field.max } : {}), id: field.id, name: field.id, value: value, onChange: value => handleChange(value, field.id), changeOnWheel: true })));
            case "transferData":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_transferData__WEBPACK_IMPORTED_MODULE_20__["default"], { field: field, handleChange: handleChange, defaultValue: value, context: context, componentService: componentService, commands: commands, nodeId: nodeId, inDialog: advanced })));
            case "dataMapping":
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { label: field.label, ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_forms_dataMapping__WEBPACK_IMPORTED_MODULE_21__["default"], { data: data, field: field, handleChange: handleChange, defaultValue: values, context: context, componentService: componentService, commands: commands, nodeId: nodeId, inDialog: advanced })));
            case "info":
                const { Paragraph } = antd__WEBPACK_IMPORTED_MODULE_1__.Typography;
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Paragraph, null, field.text));
            default:
                return null;
        }
    })));
};
function ConfigModal({ name, nodeId, form, data, context, componentService, manager, commands, handleChange, advanced, modalOpen, setModalOpen }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Modal, { title: name, centered: true, open: modalOpen, onOk: () => setModalOpen(false), onCancel: () => setModalOpen(false), width: 800, footer: (_, { OkBtn }) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(OkBtn, null))) },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form, { layout: "vertical" }, generateUIInputs({ name, nodeId, form, data, context, componentService, manager, commands, handleChange, advanced: true })))));
}


/***/ }),

/***/ "./lib/forms/CodeTextarea.js":
/*!***********************************!*\
  !*** ./lib/forms/CodeTextarea.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CodeTextarea: () => (/* binding */ CodeTextarea),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_ace__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-ace */ "webpack/sharing/consume/default/react-ace/react-ace");
/* harmony import */ var react_ace__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_ace__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var ace_builds_src_noconflict_mode_python__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ace-builds/src-noconflict/mode-python */ "../../node_modules/ace-builds/src-noconflict/mode-python.js");
/* harmony import */ var ace_builds_src_noconflict_mode_python__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(ace_builds_src_noconflict_mode_python__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var ace_builds_src_noconflict_mode_sql__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ace-builds/src-noconflict/mode-sql */ "../../node_modules/ace-builds/src-noconflict/mode-sql.js");
/* harmony import */ var ace_builds_src_noconflict_mode_sql__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(ace_builds_src_noconflict_mode_sql__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var ace_builds_src_noconflict_theme_xcode__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ace-builds/src-noconflict/theme-xcode */ "../../node_modules/ace-builds/src-noconflict/theme-xcode.js");
/* harmony import */ var ace_builds_src_noconflict_theme_xcode__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(ace_builds_src_noconflict_theme_xcode__WEBPACK_IMPORTED_MODULE_4__);





const CodeTextarea = ({ field, value, handleChange, advanced, rows }) => {
    const [inputValue, setInputValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(value);
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setInputValue(value); // Update inputValue when value prop changes
    }, [value]);
    const handleInputChange = (val) => {
        const newValue = val;
        setInputValue(newValue);
        handleChange(newValue, field.id);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react_ace__WEBPACK_IMPORTED_MODULE_1___default()), { width: '100%', height: field.height, placeholder: field.placeholder, mode: field.mode, theme: "xcode", name: field.id, onChange: handleInputChange, fontSize: 14, lineHeight: 19, showPrintMargin: true, showGutter: true, highlightActiveLine: true, value: inputValue, setOptions: {
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: true,
            showLineNumbers: true,
            tabSize: 2,
        } }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CodeTextarea);


/***/ }),

/***/ "./lib/forms/InputRegular.js":
/*!***********************************!*\
  !*** ./lib/forms/InputRegular.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   InputRegular: () => (/* binding */ InputRegular),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/EyeTwoTone.js");
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/EyeInvisibleOutlined.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _PipelineService__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../PipelineService */ "./lib/PipelineService.js");




const InputRegular = ({ field, value, handleChange, context, advanced }) => {
    const [inputValue, setInputValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(value);
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [openValue, setOpenValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setInputValue(value); // Update inputValue when value prop changes
    }, [value]);
    const handleInputChange = (value) => {
        setInputValue(value);
        handleChange(value, field.id);
    };
    const handleSelect = (value, option) => {
        const newValue = `{os.environ['${value}']}`;
        handleInputChange(newValue);
    };
    const filterOptions = (inputValue, option) => {
        if (!option || option.value === undefined) {
            console.error("Option or option.value is undefined:", option);
            return false;
        }
        if (inputValue.endsWith('{')) {
            setOpenValue(true);
            return true;
        }
        else {
            setOpenValue(false);
            const lastDollarIndex = inputValue.lastIndexOf('{');
            if (lastDollarIndex !== -1 && lastDollarIndex < inputValue.length - 1) {
                const searchTerm = inputValue.substring(lastDollarIndex + 1);
                // console.log("Option: %o", option);
                return option.value.startsWith(searchTerm);
            }
            return false;
        }
    };
    const renderTitle = (title) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, title));
    const renderItem = (title) => ({
        value: title,
        label: (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: {
                display: 'flex',
                justifyContent: 'space-between',
            } }, title)),
    });
    const options = [
        {
            label: renderTitle('Environment Variables'),
            options: _PipelineService__WEBPACK_IMPORTED_MODULE_2__.PipelineService.getEnvironmentVariables(context.model.toString()).map(variable => renderItem(variable.name)),
        }
    ];
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.AutoComplete, { ref: inputRef, id: field.id, placeholder: field.placeholder, popupClassName: "certain-category-search-dropdown", options: options, filterOption: filterOptions, size: advanced ? "middle" : "small", open: openValue, defaultOpen: false, value: inputValue, onChange: handleInputChange, onSelect: handleSelect }, field.inputType === 'password' && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input.Password, { ref: inputRef, id: field.id, size: advanced ? "middle" : "small", name: field.id, placeholder: field.placeholder, value: inputValue, autoComplete: "off", iconRender: (visible) => (visible ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null) : react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_4__["default"], null)) }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (InputRegular);


/***/ }),

/***/ "./lib/forms/TextareaRegular.js":
/*!**************************************!*\
  !*** ./lib/forms/TextareaRegular.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TextareaRegular: () => (/* binding */ TextareaRegular),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);


const { TextArea } = antd__WEBPACK_IMPORTED_MODULE_1__.Input;
const TextareaRegular = ({ field, value, handleChange, advanced, rows }) => {
    const [inputValue, setInputValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(value);
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setInputValue(value); // Update inputValue when value prop changes
    }, [value]);
    const handleInputChange = (e) => {
        const newValue = e.target.value;
        const cursorPosition = e.target.selectionStart; // Save the cursor position
        setInputValue(newValue);
        handleChange(newValue, field.id);
        // Reset cursor position after the state updates
        setTimeout(() => {
            if (inputRef.current) {
                inputRef.current.selectionStart = cursorPosition;
                inputRef.current.selectionEnd = cursorPosition;
            }
        }, 0);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(TextArea, { ref: inputRef, id: field.id, size: advanced ? "middle" : "small", name: field.id, placeholder: field.placeholder, onChange: handleInputChange, value: inputValue, autoComplete: "off", rows: rows }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (TextareaRegular);


/***/ }),

/***/ "./lib/forms/dataMapping.js":
/*!**********************************!*\
  !*** ./lib/forms/dataMapping.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DataMapping: () => (/* binding */ DataMapping),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/DeleteOutlined.js");
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/PlusOutlined.js");
/* harmony import */ var _RequestService__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../RequestService */ "./lib/RequestService.js");




const DataMapping = ({ data, field, handleChange, defaultValue, context, componentService, commands, nodeId, inDialog }) => {
    const EditableContext = react__WEBPACK_IMPORTED_MODULE_0___default().createContext(null);
    const [loadingsInput, setLoadingsInput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const [loadingsOutput, setLoadingsOutput] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const EditableRow = ({ index, ...props }) => {
        const [form] = antd__WEBPACK_IMPORTED_MODULE_1__.Form.useForm();
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form, { form: form, component: false },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(EditableContext.Provider, { value: form },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", { ...props }))));
    };
    const EditableCell = ({ title, editable, children, dataIndex, record, handleSave, ...restProps }) => {
        var _a, _b;
        const form = (0,react__WEBPACK_IMPORTED_MODULE_0__.useContext)(EditableContext);
        const [editing, setEditing] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
        const handleSelectChange = (selection, record) => {
            const value = selection.value;
            const input = items.find(item => item.value === value); // Finds the item where value matches
            record.input = input; // Assigns the found item to record.input
            handleSave(record); // Save the updated record
        };
        let childNode = children;
        if (editable) {
            childNode =
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { style: { margin: 0 }, name: dataIndex, rules: [
                        {
                            required: true,
                            message: `${title} is required.`,
                        },
                    ] },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.ConfigProvider, { renderEmpty: customizeRenderEmpty },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { showSearch: true, labelInValue: true, size: inDialog ? "middle" : "small", style: { width: '100%' }, className: "nodrag", onChange: (value) => { handleSelectChange(value, record); }, value: (_b = (_a = record.input) === null || _a === void 0 ? void 0 : _a.value) !== null && _b !== void 0 ? _b : "", placeholder: 'Select column ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), dropdownRender: (menu) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                                menu,
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '0 2px 2px' } },
                                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "primary", onClick: (event) => {
                                            _RequestService__WEBPACK_IMPORTED_MODULE_2__.RequestService.retrieveDataframeColumns(event, context, commands, componentService, setItems, setLoadingsInput, nodeId, 0, true);
                                        }, loading: loadingsInput }, "Retrieve columns")))), options: items.map((item) => ({ label: item.label, value: item.value, type: item.type, named: item.named })), optionRender: (option) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, null,
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
                                    " ",
                                    option.data.label),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Tag, null, option.data.type))) })));
        }
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("td", { ...restProps }, childNode);
    };
    const [dataSource, setDataSource] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(defaultValue || []);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        handleChange(dataSource, field.id);
    }, [dataSource]);
    const customizeRenderEmpty = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { textAlign: 'center' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Empty, { image: antd__WEBPACK_IMPORTED_MODULE_1__.Empty.PRESENTED_IMAGE_SIMPLE })));
    const defaultColumns = [
        {
            title: 'Input Columns',
            dataIndex: 'input',
            width: '50%',
            editable: true,
        },
        {
            title: 'Output Schema',
            dataIndex: 'value',
            width: '50%',
            editable: false,
            render: (_, record) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, record.value),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Tag, null, record.type))))
        },
        {
            title: '',
            dataIndex: 'operation',
            render: (_, record) => dataSource.length >= 1 ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Popconfirm, { title: "Sure to delete?", onConfirm: () => handleDelete(record.key) },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null))) : null,
        }
    ];
    const [form] = antd__WEBPACK_IMPORTED_MODULE_1__.Form.useForm(); // Step 1: Create form instance
    const handleAdd = () => {
        const values = form.getFieldsValue(); // Step 2: Get values from the form
        console.log(values); // Do something with the form data
        console.log('Received values from form: ', values);
        const newData = {
            input: {},
            key: values.field.name,
            value: values.field.name,
            type: values.field.type
        };
        setDataSource([...dataSource, newData]);
    };
    const handleSave = (row) => {
        const newData = [...dataSource];
        const index = newData.findIndex((item) => row.key === item.key);
        const item = newData[index];
        newData.splice(index, 1, {
            ...item,
            ...row,
        });
        setDataSource(newData);
    };
    const handleDelete = (key) => {
        const newData = dataSource.filter((item) => item.key !== key);
        setDataSource(newData);
    };
    const components = {
        body: {
            row: EditableRow,
            cell: EditableCell,
        },
    };
    const columns = defaultColumns.map((col) => {
        if (!col.editable) {
            return col;
        }
        return {
            ...col,
            onCell: (record) => ({
                record,
                editable: col.editable,
                dataIndex: col.dataIndex,
                title: col.title,
                handleSave,
            }),
        };
    });
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
            field.outputType === 'relationalDatabase' ? (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "primary", size: "small", style: { marginBottom: 16 }, onClick: (event) => {
                    setDataSource([]);
                    _RequestService__WEBPACK_IMPORTED_MODULE_2__.RequestService.retrieveTableColumns(event, `${field.drivers}://${data.dbOptions.username}:${data.dbOptions.password}@${data.dbOptions.host}:${data.dbOptions.port}/${data.dbOptions.databaseName}`, `${data.dbOptions.tableName}`, `DESCRIBE ${data.dbOptions.tableName}`, context, commands, componentService, setDataSource, setLoadingsOutput, nodeId);
                }, loading: loadingsOutput }, "Retrieve schema")) : null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Table, { components: components, rowClassName: () => 'editable-row', bordered: true, dataSource: dataSource, columns: columns }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form, { style: { marginTop: 16 }, name: "Add field row", layout: "inline", form: form },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, { name: "field" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(FieldValueInput, { field: field })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, null,
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { onClick: handleAdd }, "Add a field"))))));
};
const FieldValueInput = ({ field, value = {}, onChange }) => {
    const [name, setName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [type, setType] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [nameType, setNameType] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(field.typeOptions);
    const triggerChange = (changedValue) => {
        onChange === null || onChange === void 0 ? void 0 : onChange({ name, type, ...value, ...changedValue });
    };
    const onNameChange = (e) => {
        const newName = e.target.value || '';
        setName(newName);
        triggerChange({ name: newName });
    };
    const onTypeChange = (newType) => {
        setType(newType);
        triggerChange({ type: newType });
    };
    const onNameTypeChange = (event) => {
        setNameType(event.target.value);
    };
    const addItem = (e) => {
        e.preventDefault();
        setItems([...items, { value: name, label: name }]);
        setName('');
        setTimeout(() => {
            var _a;
            (_a = inputRef.current) === null || _a === void 0 ? void 0 : _a.focus();
        }, 0);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { type: "text", value: name, placeholder: 'Field name', onChange: onNameChange, style: { width: 150 } }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { value: type, style: { width: 220, margin: '0 8px' }, className: "nodrag", onChange: onTypeChange, dropdownRender: (menu) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                menu,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { padding: '0 8px 4px' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { placeholder: "Custom", ref: inputRef, value: nameType, onChange: onNameTypeChange, onKeyDown: (e) => e.stopPropagation() }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "text", icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_4__["default"], null), onClick: addItem }, "Add type")))), options: items.map((item) => ({ label: item.value, value: item.value })) })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (DataMapping);


/***/ }),

/***/ "./lib/forms/keyValueColumns.js":
/*!**************************************!*\
  !*** ./lib/forms/keyValueColumns.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   KeyValueColumns: () => (/* binding */ KeyValueColumns),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/PlusOutlined.js");
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/MinusCircleOutlined.js");
/* harmony import */ var _RequestService__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../RequestService */ "./lib/RequestService.js");




const KeyValueColumns = ({ field, handleChange, initialValues, context, componentService, commands, nodeId, inDialog }) => {
    const [keyValuePairs, setKeyValuePairs] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(initialValues || [{ key: { value: '', type: '', named: true }, value: '' }]);
    const [loadings, setLoadings] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [name, setName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const handleAddPair = () => {
        setKeyValuePairs([...keyValuePairs, { key: '', value: '' }]);
        handleChange(keyValuePairs, field.id);
    };
    const handleRemovePair = (index) => {
        const pairs = [...keyValuePairs];
        pairs.splice(index, 1);
        setKeyValuePairs(pairs);
        handleChange(pairs, field.id);
    };
    const handleChangeKV = (e, index, property) => {
        const updatedKeyValuePairs = [...keyValuePairs];
        updatedKeyValuePairs[index] = {
            ...updatedKeyValuePairs[index],
            [property]: e.target.value
        };
        setKeyValuePairs(updatedKeyValuePairs);
        handleChange(updatedKeyValuePairs, field.id);
    };
    const getAvailableItems = (index) => {
        const selectedKeys = keyValuePairs.map(pair => pair.key).filter((_, idx) => idx !== index);
        return items ? items.filter(item => !selectedKeys.includes(item.value)) : [];
    };
    const getTypeNamedByValue = (items, value) => {
        const item = items.find(item => item.value === value);
        if (item) {
            return { type: item.type, named: item.named };
        }
        return undefined;
    };
    const onNameChange = (event) => {
        setName(event.target.value);
    };
    const handleSelectChange = (selection, index) => {
        const value = selection.value;
        const { type, named } = getTypeNamedByValue(items, value);
        const updatedKeyValuePairs = [...keyValuePairs];
        updatedKeyValuePairs[index] = {
            ...updatedKeyValuePairs[index],
            key: { value: value, type: type, named: named }
        };
        setKeyValuePairs(updatedKeyValuePairs);
        handleChange(updatedKeyValuePairs, field.id);
    };
    const customizeRenderEmpty = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { textAlign: 'center' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Empty, { image: antd__WEBPACK_IMPORTED_MODULE_1__.Empty.PRESENTED_IMAGE_SIMPLE }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "primary", onClick: (event) => _RequestService__WEBPACK_IMPORTED_MODULE_2__.RequestService.retrieveDataframeColumns(event, context, commands, componentService, setItems, setLoadings, nodeId, 0, true), loading: loadings }, "Retrieve columns")));
    const addItem = (e) => {
        e.preventDefault();
        setItems([...items, { value: name, label: name }]);
        setName('');
        setTimeout(() => {
            var _a;
            (_a = inputRef.current) === null || _a === void 0 ? void 0 : _a.focus();
        }, 0);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.List, { name: "keyValue" }, (fields, { add, remove }) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, null, keyValuePairs.map((pair, index) => {
            var _a;
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { display: 'flex', width: '100%', marginBottom: 8 }, align: "baseline" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.ConfigProvider, { renderEmpty: customizeRenderEmpty },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { labelInValue: true, size: inDialog ? "middle" : "small", style: { width: '100%', minWidth: '250px' }, className: "nodrag", onChange: (value) => { handleSelectChange(value, index); }, value: pair.key, options: getAvailableItems(index).map(item => ({ label: item.label, value: item.value })), placeholder: field.placeholder || 'Select ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), dropdownRender: (menu) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                            menu,
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { padding: '0 8px 4px' } },
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { size: inDialog ? "middle" : "small", placeholder: "Custom", ref: inputRef, value: name, onChange: onNameChange, onKeyDown: (e) => e.stopPropagation() }),
                                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "text", icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null), onClick: addItem }, "Add item")))) })),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { size: inDialog ? "middle" : "small", name: `${field.id}_value_${index}`, placeholder: ((_a = field.placeholder) === null || _a === void 0 ? void 0 : _a.value) || 'value', id: `${field.id}_value_${index}`, value: pair.value, onChange: (e) => handleChangeKV(e, index, 'value'), autoComplete: "off" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_4__["default"], { onClick: () => handleRemovePair(index) })));
        })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "dashed", onClick: handleAddPair, block: true, icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null) },
                "Add ",
                field.elementName ? field.elementName : 'item'))))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KeyValueColumns);


/***/ }),

/***/ "./lib/forms/keyValueColumnsSelect.js":
/*!********************************************!*\
  !*** ./lib/forms/keyValueColumnsSelect.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   KeyValueColumnsSelect: () => (/* binding */ KeyValueColumnsSelect),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/PlusOutlined.js");
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/MinusCircleOutlined.js");
/* harmony import */ var _RequestService__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../RequestService */ "./lib/RequestService.js");




const KeyValueColumnsSelect = ({ field, handleChange, initialValues, context, componentService, commands, nodeId, inDialog }) => {
    const [keyValuePairs, setKeyValuePairs] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(initialValues || [{ key: { value: '', type: '', named: true }, value: '' }]);
    const [loadings, setLoadings] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [options, setOptions] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(field.options);
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [name, setName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const findOptionByValue = (value) => {
        return field.options.find(option => option.value === value) || { value: value, label: value };
    };
    const handleAddPair = () => {
        setKeyValuePairs([...keyValuePairs, { key: '', value: '' }]);
        handleChange(keyValuePairs, field.id);
    };
    const handleRemovePair = (index) => {
        const pairs = [...keyValuePairs];
        pairs.splice(index, 1);
        setKeyValuePairs(pairs);
        handleChange(pairs, field.id);
    };
    const handleChangeKV = (newValue, index, property) => {
        const updatedKeyValuePairs = [...keyValuePairs];
        updatedKeyValuePairs[index] = {
            ...updatedKeyValuePairs[index],
            [property]: newValue
        };
        setKeyValuePairs(updatedKeyValuePairs);
        handleChange(updatedKeyValuePairs, field.id);
    };
    const getAvailableItems = (index) => {
        const selectedKeys = keyValuePairs.map(pair => pair.key).filter((_, idx) => idx !== index);
        return items ? items.filter(item => !selectedKeys.includes(item.value)) : [];
    };
    const getTypeNamedByValue = (items, value) => {
        const item = items.find(item => item.value === value);
        if (item) {
            return { type: item.type, named: item.named };
        }
        return undefined;
    };
    const onNameChange = (event) => {
        setName(event.target.value);
    };
    const handleSelectColumnChange = (selection, index) => {
        const value = selection.value;
        const { type, named } = getTypeNamedByValue(items, value);
        const updatedKeyValuePairs = [...keyValuePairs];
        updatedKeyValuePairs[index] = {
            ...updatedKeyValuePairs[index],
            key: { value: value, type: type, named: named }
        };
        setKeyValuePairs(updatedKeyValuePairs);
        handleChange(updatedKeyValuePairs, field.id);
    };
    const customizeRenderEmpty = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { textAlign: 'center' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Empty, { image: antd__WEBPACK_IMPORTED_MODULE_1__.Empty.PRESENTED_IMAGE_SIMPLE }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "primary", onClick: (event) => _RequestService__WEBPACK_IMPORTED_MODULE_2__.RequestService.retrieveDataframeColumns(event, context, commands, componentService, setItems, setLoadings, nodeId, 0, true), loading: loadings }, "Retrieve columns")));
    const addItem = (e) => {
        e.preventDefault();
        setItems([...items, { value: name, label: name }]);
        setName('');
        setTimeout(() => {
            var _a;
            (_a = inputRef.current) === null || _a === void 0 ? void 0 : _a.focus();
        }, 0);
    };
    console.log("placeholder " + field.placeholder);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.List, { name: "keyValue" }, (fields, { add, remove }) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, null, keyValuePairs.map((pair, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { direction: "vertical", style: { display: 'flex', width: '100%', marginBottom: 8 } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.ConfigProvider, { renderEmpty: customizeRenderEmpty },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { labelInValue: true, size: inDialog ? "middle" : "small", className: "nodrag", onChange: (value) => { handleSelectColumnChange(value, index); }, value: pair.key, options: getAvailableItems(index).map(item => ({ label: item.label, value: item.value })), placeholder: 'Select ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), dropdownRender: (menu) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                        menu,
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { padding: '0 8px 4px' } },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { size: inDialog ? "middle" : "small", placeholder: "Custom", ref: inputRef, value: name, onChange: onNameChange, onKeyDown: (e) => e.stopPropagation() }),
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "text", icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null), onClick: addItem }, "Add item")))) })),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { labelInValue: true, size: inDialog ? "middle" : "small", id: `${field.id}_value_${index}`, className: "nodrag", onChange: (value) => handleChangeKV(value, index, 'value'), value: pair.value, placeholder: "Select ...", ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), options: options.map(option => ({
                    label: option.label,
                    value: option.value
                })) }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_4__["default"], { onClick: () => handleRemovePair(index) }))))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "dashed", onClick: handleAddPair, block: true, icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null) },
                "Add ",
                field.elementName ? field.elementName : 'item'))))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KeyValueColumnsSelect);


/***/ }),

/***/ "./lib/forms/keyValueForm.js":
/*!***********************************!*\
  !*** ./lib/forms/keyValueForm.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   KeyValueForm: () => (/* binding */ KeyValueForm),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/MinusCircleOutlined.js");
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/PlusOutlined.js");



const KeyValueForm = ({ field, handleChange, initialValues }) => {
    const [keyValuePairs, setKeyValuePairs] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(initialValues || [{ key: '', value: '' }]);
    const handleAddPair = () => {
        setKeyValuePairs([...keyValuePairs, { key: '', value: '' }]);
        handleChange(keyValuePairs, field.id);
    };
    const handleRemovePair = (index) => {
        const pairs = [...keyValuePairs];
        pairs.splice(index, 1);
        setKeyValuePairs(pairs);
        handleChange(pairs, field.id);
    };
    const handleChangeKV = (e, index, property) => {
        const updatedKeyValuePairs = [...keyValuePairs];
        updatedKeyValuePairs[index] = {
            ...updatedKeyValuePairs[index],
            [property]: e.target.value
        };
        setKeyValuePairs(updatedKeyValuePairs);
        handleChange(updatedKeyValuePairs, field.id);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.List, { name: "keyValue" }, (fields, { add, remove }) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, null, keyValuePairs.map((pair, index) => {
            var _a, _b;
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { display: 'flex', marginBottom: 8 }, align: "baseline" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { name: `${field.id}_key_${index}`, placeholder: ((_a = field.placeholder) === null || _a === void 0 ? void 0 : _a.key) || 'key', id: `${field.id}_key_${index}`, value: pair.key, onChange: (e) => handleChangeKV(e, index, 'key'), autoComplete: "off" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { name: `${field.id}_value_${index}`, placeholder: ((_b = field.placeholder) === null || _b === void 0 ? void 0 : _b.value) || 'value', id: `${field.id}_value_${index}`, value: pair.value, onChange: (e) => handleChangeKV(e, index, 'value'), autoComplete: "off" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_2__["default"], { onClick: () => handleRemovePair(index) })));
        })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Form.Item, null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "dashed", onClick: handleAddPair, block: true, icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null) },
                "Add ",
                field.elementName ? field.elementName : 'item'))))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KeyValueForm);


/***/ }),

/***/ "./lib/forms/selectColumn.js":
/*!***********************************!*\
  !*** ./lib/forms/selectColumn.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SelectColumn: () => (/* binding */ SelectColumn),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/PlusOutlined.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _RequestService__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../RequestService */ "./lib/RequestService.js");




const SelectColumn = ({ field, handleChange, defaultValue, context, componentService, commands, nodeId, inDialog }) => {
    const findOptionByValue = (value) => {
        if (value === undefined) {
            return {};
        }
        else {
            return items.find(option => option.value === value.value) || { value: value.value, label: value.value };
        }
    };
    const getTypeNamedByValue = (items, value) => {
        const item = items.find(item => item.value === value);
        if (item) {
            return { type: item.type, named: item.named };
        }
        return undefined;
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setSelectedOption(findOptionByValue(defaultValue));
    }, [defaultValue, field.options]);
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [name, setName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [selectedOption, setSelectedOption] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(findOptionByValue(defaultValue));
    const [loadings, setLoadings] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const inputNb = field.inputNb ? field.inputNb - 1 : 0;
    const addItem = (e) => {
        e.preventDefault();
        setItems([...items, { value: name, label: name, type: 'object', named: true }]);
        setName('');
        setTimeout(() => {
            var _a;
            (_a = inputRef.current) === null || _a === void 0 ? void 0 : _a.focus();
        }, 0);
    };
    const handleSelectChange = (selection, option) => {
        const value = selection.value;
        const selectedOption = findOptionByValue(value);
        setSelectedOption(selectedOption);
        const { type, named } = getTypeNamedByValue(items, value);
        handleChange({ value, type, named }, field.id);
    };
    const onNameChange = (event) => {
        setName(event.target.value);
    };
    const customizeRenderEmpty = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { textAlign: 'center' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Empty, { image: antd__WEBPACK_IMPORTED_MODULE_1__.Empty.PRESENTED_IMAGE_SIMPLE })));
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.ConfigProvider, { renderEmpty: customizeRenderEmpty },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { showSearch: true, labelInValue: true, size: inDialog ? "middle" : "small", style: { width: '100%' }, className: "nodrag", onChange: (value, option) => handleSelectChange(value, option), value: selectedOption, placeholder: field.placeholder || 'Select ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), dropdownRender: (menu) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                menu,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '0 2px 2px' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "primary", onClick: (event) => _RequestService__WEBPACK_IMPORTED_MODULE_2__.RequestService.retrieveDataframeColumns(event, context, commands, componentService, setItems, setLoadings, nodeId, inputNb, true), loading: loadings }, "Retrieve columns")),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { padding: '0 8px 4px' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { placeholder: "Column", ref: inputRef, value: name, onChange: onNameChange, onKeyDown: (e) => e.stopPropagation() }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "text", icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null), onClick: addItem }, "Add")))), options: items.map((item) => ({ label: item.label, value: item.value, type: item.type, named: item.named })), optionRender: (option) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
                    " ",
                    option.data.label),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Tag, null, option.data.type))) })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SelectColumn);


/***/ }),

/***/ "./lib/forms/selectColumns.js":
/*!************************************!*\
  !*** ./lib/forms/selectColumns.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SelectColumns: () => (/* binding */ SelectColumns),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/PlusOutlined.js");
/* harmony import */ var _RequestService__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../RequestService */ "./lib/RequestService.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);




const SelectColumns = ({ field, handleChange, defaultValues, context, componentService, commands, nodeId, inDialog }) => {
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(field.options || []);
    const [selectedOptions, setSelectedOptions] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(defaultValues);
    const [name, setName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [loadings, setLoadings] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    const inputNb = field.inputNb ? field.inputNb - 1 : 0;
    const getTypeNamedByValue = (items, value) => {
        const item = items.find(item => item.value === value);
        if (item) {
            return { type: item.type, named: item.named };
        }
        return undefined;
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setSelectedOptions(defaultValues);
    }, [defaultValues]);
    const addItem = (e) => {
        e.preventDefault();
        setItems([...items, { value: name, label: name, type: 'object', named: true }]);
        setName('');
        setTimeout(() => {
            var _a;
            (_a = inputRef.current) === null || _a === void 0 ? void 0 : _a.focus();
        }, 0);
    };
    const handleSelectChange = (selectedItems) => {
        setSelectedOptions(selectedItems);
        const options = selectedItems.map(item => ({
            ...getTypeNamedByValue(items, item.value),
            value: item.value
        }));
        handleChange(options, field.id);
    };
    const onNameChange = (event) => {
        setName(event.target.value);
    };
    const customizeRenderEmpty = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { textAlign: 'center' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Empty, { image: antd__WEBPACK_IMPORTED_MODULE_1__.Empty.PRESENTED_IMAGE_SIMPLE })));
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.ConfigProvider, { renderEmpty: customizeRenderEmpty },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { showSearch: true, mode: "multiple", labelInValue: true, size: inDialog ? "middle" : "small", style: { width: '100%' }, className: "nodrag", onChange: handleSelectChange, value: selectedOptions, placeholder: field.placeholder || 'Select ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), dropdownRender: (menu) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                menu,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '0 2px 2px' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "primary", onClick: (event) => _RequestService__WEBPACK_IMPORTED_MODULE_2__.RequestService.retrieveDataframeColumns(event, context, commands, componentService, setItems, setLoadings, nodeId, inputNb, true), loading: loadings }, "Retrieve columns")),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { padding: '0 8px 4px' } },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { placeholder: "Custom", ref: inputRef, value: name, onChange: onNameChange, onKeyDown: (e) => e.stopPropagation() }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "text", icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], null), onClick: addItem }, "Add column")))), options: items.map((item) => ({ label: item.label, value: item.value, type: item.type })), optionRender: (option) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null,
                    " ",
                    option.data.label),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Tag, null, option.data.type))) })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SelectColumns);


/***/ }),

/***/ "./lib/forms/selectCustomizable.js":
/*!*****************************************!*\
  !*** ./lib/forms/selectCustomizable.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SelectCustomizable: () => (/* binding */ SelectCustomizable),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/PlusOutlined.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);



const SelectCustomizable = ({ field, handleChange, defaultValue, inDialog }) => {
    const findOptionByValue = (value) => {
        return field.options.find(option => option.value === value) || { value: value, label: value };
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setSelectedOption(findOptionByValue(defaultValue));
    }, [defaultValue, field.options]);
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(field.options);
    const [name, setName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const inputRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const [selectedOption, setSelectedOption] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(findOptionByValue(defaultValue));
    let index = 0;
    const addItem = (e) => {
        e.preventDefault();
        setItems([...items, { value: name, label: name }]);
        setName('');
        setTimeout(() => {
            var _a;
            (_a = inputRef.current) === null || _a === void 0 ? void 0 : _a.focus();
        }, 0);
    };
    const handleSelectChange = (option) => {
        setSelectedOption(option);
        handleChange(option === null || option === void 0 ? void 0 : option.value, field.id);
    };
    const onNameChange = (event) => {
        setName(event.target.value);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { labelInValue: true, size: inDialog ? "middle" : "small", style: { width: '100%' }, className: "nodrag", onChange: handleSelectChange, value: selectedOption, placeholder: field.placeholder || 'Select ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), dropdownRender: (menu) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            menu,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Divider, { style: { margin: '8px 0' } }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Space, { style: { padding: '0 8px 4px' } },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Input, { placeholder: "Custom", ref: inputRef, value: name, onChange: onNameChange, onKeyDown: (e) => e.stopPropagation() }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Button, { type: "text", icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_2__["default"], null), onClick: addItem }, "Add item")))), options: items.map((item) => ({ label: item.label, value: item.value })) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SelectCustomizable);


/***/ }),

/***/ "./lib/forms/selectRegular.js":
/*!************************************!*\
  !*** ./lib/forms/selectRegular.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SelectRegular: () => (/* binding */ SelectRegular),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);


const SelectRegular = ({ field, handleChange, defaultValue, inDialog }) => {
    const findOptionByValue = (value) => {
        return field.options.find(option => option.value === value) || { value: value, label: value };
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setSelectedOption(findOptionByValue(defaultValue));
    }, [defaultValue, field.options]);
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(field.options);
    const [selectedOption, setSelectedOption] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(findOptionByValue(defaultValue));
    const handleSelectChange = (option) => {
        setSelectedOption(option);
        handleChange(option === null || option === void 0 ? void 0 : option.value, field.id);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { labelInValue: true, size: inDialog ? "middle" : "small", style: { width: '100%' }, className: "nodrag", onChange: handleSelectChange, value: selectedOption, placeholder: field.placeholder || 'Select ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), options: items.map(item => ({
            label: item.label,
            value: item.value
        })) }));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SelectRegular);


/***/ }),

/***/ "./lib/forms/selectTokenization.js":
/*!*****************************************!*\
  !*** ./lib/forms/selectTokenization.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SelectTokenization: () => (/* binding */ SelectTokenization),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);


const SelectTokenization = ({ field, handleChange, defaultValue, inDialog }) => {
    // Assuming defaultValues are already in the correct format
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        setSelectedOptions(defaultValue);
    }, [defaultValue]);
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(field.options);
    const [selectedOptions, setSelectedOptions] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(defaultValue);
    const handleSelectChange = (selectedItems) => {
        setSelectedOptions(selectedItems);
        handleChange(selectedItems.map(item => item.value), field.id);
    };
    const customizeRenderEmpty = () => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", { style: { display: 'none' } }));
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.ConfigProvider, { renderEmpty: customizeRenderEmpty },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Select, { mode: "tags", labelInValue: true, size: inDialog ? "middle" : "small", style: { width: '100%' }, className: "nodrag", onChange: handleSelectChange, value: selectedOptions, tokenSeparators: [','], placeholder: field.placeholder || 'Select ...', ...(field.required ? { required: field.required } : {}), ...(field.tooltip ? { tooltip: field.tooltip } : {}), options: items.map(item => ({
                label: item.label,
                value: item.value
            })) })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (SelectTokenization);


/***/ }),

/***/ "./lib/forms/transferData.js":
/*!***********************************!*\
  !*** ./lib/forms/transferData.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   TransferData: () => (/* binding */ TransferData),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_dnd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-dnd */ "webpack/sharing/consume/default/react-dnd/react-dnd");
/* harmony import */ var react_dnd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_dnd__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _RequestService__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../RequestService */ "./lib/RequestService.js");
/* harmony import */ var _DndProviderWrapper__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../DndProviderWrapper */ "./lib/DndProviderWrapper.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_2__);





const TransferData = ({ field, handleChange, defaultValue, context, componentService, commands, nodeId, inDialog }) => {
    const DragableBodyRow = ({ index, rowDrop, className, style, ...restProps }) => {
        const ref = react__WEBPACK_IMPORTED_MODULE_0___default().useRef();
        const [{ isOver, dropClassName }, drop] = (0,react_dnd__WEBPACK_IMPORTED_MODULE_1__.useDrop)({
            accept: 'DragableBodyRow',
            collect: (monitor) => {
                const item = monitor.getItem(); // Cast to DragItem
                if (item && item.index === index) {
                    return {};
                }
                return {
                    isOver: monitor.isOver(),
                    dropClassName: item && item.index < index ? ' drop-over-downward' : ' drop-over-upward',
                };
            },
            drop: (item) => {
                rowDrop(item.index, index);
            },
        });
        const [, drag] = (0,react_dnd__WEBPACK_IMPORTED_MODULE_1__.useDrag)({
            type: 'DragableBodyRow',
            item: { type: 'DragableBodyRow', index },
            collect: (monitor) => ({
                isDragging: monitor.isDragging(),
            }),
        });
        drag(drop(ref));
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("tr", { ref: ref, className: `${className}${isOver ? dropClassName : ''} draggable`, style: { cursor: 'move', opacity: isOver ? 0.5 : 1, ...style }, ...restProps }));
    };
    // Customize Table Transfer
    const TableTransfer = ({ leftColumns, rightColumns, ...restProps }) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_2__.Transfer, { ...restProps }, ({ direction, filteredItems, onItemSelect, onItemSelectAll, selectedKeys: listSelectedKeys, disabled: listDisabled, }) => {
        const columns = direction === 'left' ? leftColumns : rightColumns;
        const displayType = direction === 'right' ? 'target' : 'source';
        const rowSelection = {
            getCheckboxProps: () => ({ disabled: listDisabled }),
            onChange(selectedRowKeys) {
                onItemSelectAll(selectedRowKeys, 'replace');
            },
            selectedRowKeys: listSelectedKeys,
            selections: [antd__WEBPACK_IMPORTED_MODULE_2__.Table.SELECTION_ALL, antd__WEBPACK_IMPORTED_MODULE_2__.Table.SELECTION_INVERT, antd__WEBPACK_IMPORTED_MODULE_2__.Table.SELECTION_NONE],
        };
        if (displayType === 'source') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_2__.Table, { rowSelection: rowSelection, columns: columns, dataSource: filteredItems, size: "small", style: { pointerEvents: listDisabled ? 'none' : undefined }, onRow: ({ key, disabled: itemDisabled }) => ({
                    onClick: () => {
                        if (itemDisabled || listDisabled) {
                            return;
                        }
                        onItemSelect(key, !listSelectedKeys.includes(key));
                    },
                }) }));
        }
        else {
            const rowDrop = (dragIndex, hoverIndex) => {
                console.log("dragIndex:", dragIndex);
                console.log("hoverIndex:", hoverIndex);
                // Ensure the indices are valid
                if (dragIndex === undefined || hoverIndex === undefined) {
                    console.error("Invalid drag or hover index");
                    return;
                }
                // Create a copy of the target keys with all properties intact
                let newKeys = [...targetKeys];
                console.log("Initial newKeys:", newKeys);
                // Extract the dragged item and re-insert at the hover index
                const dragRow = newKeys.splice(dragIndex, 1)[0]; // Ensure correct extraction
                newKeys.splice(hoverIndex, 0, dragRow); // Insert at the correct position
                console.log("Updated newKeys:", newKeys);
                setTargetKeys(newKeys);
                const savedSchema = { sourceData: sourceData, targetKeys: newKeys };
                handleChange(savedSchema, field.id);
            };
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_DndProviderWrapper__WEBPACK_IMPORTED_MODULE_3__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_2__.Table, { rowSelection: rowSelection, columns: columns, dataSource: filteredItems, components: {
                        body: {
                            row: DragableBodyRow,
                        },
                    }, size: "small", style: { pointerEvents: listDisabled ? 'none' : undefined }, onRow: (record, idx) => ({
                        index: idx,
                        rowDrop,
                        onClick: () => {
                            if (record.disabled) {
                                return;
                            }
                            onItemSelect(record.key, !listSelectedKeys.includes(record.key)); // Toggle selection
                        },
                    }) })));
        }
    }));
    const [items, setItems] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [sourceData, setSourceData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [targetKeys, setTargetKeys] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)([]);
    const [loadings, setLoadings] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)();
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        console.log("Transfer Data, items %o", items);
        setSourceData(items.map(item => ({
            ...item,
            key: item.value,
            title: item.value
        })));
    }, [items]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        if (defaultValue && defaultValue.sourceData && defaultValue.targetKeys) {
            setSourceData(defaultValue.sourceData);
            setTargetKeys(defaultValue.targetKeys);
        }
        else {
            // Provide default initialization for sourceData and targetKeys if defaultValue doesn't exist
            setSourceData([]);
            setTargetKeys([]);
        }
    }, [defaultValue]);
    const columns = [
        {
            dataIndex: 'value',
            title: 'Column',
        },
        {
            dataIndex: 'type',
            title: 'Type',
            render: (type) => react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_2__.Tag, null, type),
        }
    ];
    const onChange = (nextTargetKeys) => {
        console.log("newTargetKeys %o", nextTargetKeys);
        setTargetKeys(nextTargetKeys);
        const savedSchema = { sourceData: sourceData, targetKeys: nextTargetKeys };
        handleChange(savedSchema, field.id);
    };
    const renderFooter = (_, info) => {
        if ((info === null || info === void 0 ? void 0 : info.direction) === 'left') {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_2__.Button, { type: "primary", size: "small", style: { float: 'left', margin: 5 }, onClick: (event) => _RequestService__WEBPACK_IMPORTED_MODULE_4__.RequestService.retrieveDataframeColumns(event, context, commands, componentService, setItems, setLoadings, nodeId, 0, true), loading: loadings }, "Retrieve columns"));
        }
        return;
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(TableTransfer, { dataSource: sourceData, targetKeys: targetKeys, showSearch: true, onChange: onChange, operations: ['include', 'exclude'], filterOption: (inputValue, item) => item.key.indexOf(inputValue) !== -1 || item.type.indexOf(inputValue) !== -1, leftColumns: columns, rightColumns: columns, footer: renderFooter }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_2__.Space, { style: { marginTop: 16 } })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (TransferData);


/***/ }),

/***/ "./lib/forms/valuesListForm.js":
/*!*************************************!*\
  !*** ./lib/forms/valuesListForm.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ValuesListForm: () => (/* binding */ ValuesListForm),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../icons */ "./lib/icons.js");


const ValuesListForm = ({ field, handleChange, initialValues }) => {
    const [values, setValues] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(initialValues || ['']);
    const handleAddValue = () => {
        setValues([...values, '']);
        handleChange(values, field.id);
    };
    const handleRemoveValue = (index) => {
        const updatedValues = [...values];
        updatedValues.splice(index, 1);
        setValues(updatedValues);
        handleChange(updatedValues, field.id);
    };
    const handleChangeValue = (e, index) => {
        const updatedValues = [...values];
        updatedValues[index] = e.target.value;
        setValues(updatedValues);
        handleChange(updatedValues, field.id);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        values.map((value, index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { key: index, className: "flex items-center space-x-2" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "text", name: `${field.id}_value_${index}`, placeholder: "Value", id: `${field.id}_value_${index}`, value: value, onChange: (e) => handleChangeValue(e, index), className: "mt-1 h-6 w-full rounded-sm border-gray-200 shadow-sm sm:text-xs" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: () => handleRemoveValue(index), className: "nodrag flex flex-col justify-center items-center mt-1 w-9 h-6 rounded-sm bg-gray-500 text-white shadow-sm sm:text-xs" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_1__.minusIcon.react, { className: "" }))))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: handleAddValue, className: "nodrag flex flex-col justify-center items-center mt-2 w-9 h-6 rounded-sm bg-gray-500 text-white shadow-sm sm:text-xs" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_1__.plusIcon.react, { className: "" }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ValuesListForm);


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   crosshairIcon: () => (/* binding */ crosshairIcon),
/* harmony export */   minusIcon: () => (/* binding */ minusIcon),
/* harmony export */   playCircleIcon: () => (/* binding */ playCircleIcon),
/* harmony export */   playIcon: () => (/* binding */ playIcon),
/* harmony export */   plusIcon: () => (/* binding */ plusIcon),
/* harmony export */   searchIcon: () => (/* binding */ searchIcon),
/* harmony export */   settingsIcon: () => (/* binding */ settingsIcon),
/* harmony export */   trashIcon: () => (/* binding */ trashIcon),
/* harmony export */   warningIcon: () => (/* binding */ warningIcon),
/* harmony export */   xIcon: () => (/* binding */ xIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_trash_16_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/trash-16.svg */ "./style/icons/trash-16.svg");
/* harmony import */ var _style_icons_x_16_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/icons/x-16.svg */ "./style/icons/x-16.svg");
/* harmony import */ var _style_icons_settings_16_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/icons/settings-16.svg */ "./style/icons/settings-16.svg");
/* harmony import */ var _style_icons_search_16_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/search-16.svg */ "./style/icons/search-16.svg");
/* harmony import */ var _style_icons_crosshair_16_svg__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../style/icons/crosshair-16.svg */ "./style/icons/crosshair-16.svg");
/* harmony import */ var _style_icons_minus_16_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icons/minus-16.svg */ "./style/icons/minus-16.svg");
/* harmony import */ var _style_icons_plus_16_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/icons/plus-16.svg */ "./style/icons/plus-16.svg");
/* harmony import */ var _style_icons_play_16_svg__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/icons/play-16.svg */ "./style/icons/play-16.svg");
/* harmony import */ var _style_icons_play_circle_16_svg__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/icons/play-circle-16.svg */ "./style/icons/play-circle-16.svg");
/* harmony import */ var _style_icons_alert_triangle_fill_16_svg__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../style/icons/alert-triangle-fill-16.svg */ "./style/icons/alert-triangle-fill-16.svg");











const trashIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:trash-icon',
    svgstr: _style_icons_trash_16_svg__WEBPACK_IMPORTED_MODULE_1__
});
const xIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:cog-icon',
    svgstr: _style_icons_x_16_svg__WEBPACK_IMPORTED_MODULE_2__
});
const settingsIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:settings-icon',
    svgstr: _style_icons_settings_16_svg__WEBPACK_IMPORTED_MODULE_3__
});
const searchIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:search-icon',
    svgstr: _style_icons_search_16_svg__WEBPACK_IMPORTED_MODULE_4__
});
const minusIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:minus-icon',
    svgstr: _style_icons_minus_16_svg__WEBPACK_IMPORTED_MODULE_5__
});
const plusIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:plus-icon',
    svgstr: _style_icons_plus_16_svg__WEBPACK_IMPORTED_MODULE_6__
});
const playIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:play-icon',
    svgstr: _style_icons_play_16_svg__WEBPACK_IMPORTED_MODULE_7__
});
const playCircleIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:play-circle-icon',
    svgstr: _style_icons_play_circle_16_svg__WEBPACK_IMPORTED_MODULE_8__
});
const crosshairIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:crosshair-icon',
    svgstr: _style_icons_crosshair_16_svg__WEBPACK_IMPORTED_MODULE_9__
});
const warningIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:warning-icon',
    svgstr: _style_icons_alert_triangle_fill_16_svg__WEBPACK_IMPORTED_MODULE_10__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   CodeGenerator: () => (/* reexport safe */ _CodeGenerator__WEBPACK_IMPORTED_MODULE_4__.CodeGenerator),
/* harmony export */   ComponentManager: () => (/* binding */ ComponentManager),
/* harmony export */   PipelineComponent: () => (/* reexport safe */ _PipelineComponent__WEBPACK_IMPORTED_MODULE_3__.PipelineComponent),
/* harmony export */   PipelineService: () => (/* reexport safe */ _PipelineService__WEBPACK_IMPORTED_MODULE_5__.PipelineService),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   generateUIFormComponent: () => (/* reexport safe */ _configUtils__WEBPACK_IMPORTED_MODULE_1__.generateUIFormComponent),
/* harmony export */   onChange: () => (/* reexport safe */ _configUtils__WEBPACK_IMPORTED_MODULE_1__.onChange),
/* harmony export */   renderComponentUI: () => (/* reexport safe */ _rendererUtils__WEBPACK_IMPORTED_MODULE_2__.renderComponentUI),
/* harmony export */   renderHandle: () => (/* reexport safe */ _rendererUtils__WEBPACK_IMPORTED_MODULE_2__.renderHandle),
/* harmony export */   setDefaultConfig: () => (/* reexport safe */ _configUtils__WEBPACK_IMPORTED_MODULE_1__.setDefaultConfig)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _configUtils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./configUtils */ "./lib/configUtils.js");
/* harmony import */ var _rendererUtils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./rendererUtils */ "./lib/rendererUtils.js");
/* harmony import */ var _PipelineComponent__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./PipelineComponent */ "./lib/PipelineComponent.js");
/* harmony import */ var _CodeGenerator__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./CodeGenerator */ "./lib/CodeGenerator.js");
/* harmony import */ var _PipelineService__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./PipelineService */ "./lib/PipelineService.js");






const ComponentManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@amphi/pipeline-components-manager:provider');
class ComponentService {
    constructor() {
        this._components = [];
        this._components = [];
    }
    getComponents() {
        return this._components;
    }
    ;
    getComponent(id) {
        return this._components.find(component => component._id === id);
    }
    ;
    addComponent(newComponent) {
        this._components.push(newComponent);
    }
    ;
    // Method to get the number of components
    getComponentCount() {
        return this._components.length;
    }
}
const plugin = {
    id: '@amphi/pipeline-components-manager:plugin',
    description: 'Provider plugin for the pipeline editor\'s "component" service object.',
    autoStart: true,
    provides: ComponentManager,
    activate: () => {
        console.log('JupyterLab extension (@amphi/pipeline-components-manager/provider plugin) is activated!');
        const componentService = new ComponentService();
        return componentService;
    }
};

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/rendererUtils.js":
/*!******************************!*\
  !*** ./lib/rendererUtils.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   renderComponentUI: () => (/* binding */ renderComponentUI),
/* harmony export */   renderHandle: () => (/* binding */ renderHandle)
/* harmony export */ });
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _ant_design_icons__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @ant-design/icons */ "../../node_modules/@ant-design/icons/es/icons/QuestionCircleOutlined.js");
/* harmony import */ var reactflow__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! reactflow */ "../../node_modules/reactflow/node_modules/@reactflow/core/dist/esm/index.js");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_1__);
// ConfigForm.tsx





const renderHandle = ({ type, Handle, Position, internals }) => {
    const LimitedInputHandle = (props) => {
        const { nodeInternals, edges, nodeId } = internals;
        const isHandleConnectable = (0,react__WEBPACK_IMPORTED_MODULE_0__.useMemo)(() => {
            if (typeof props.isConnectable === 'function') {
                const node = nodeInternals.get(nodeId);
                const connectedEdges = (0,reactflow__WEBPACK_IMPORTED_MODULE_2__.getConnectedEdges)([node], edges).filter(edge => edge.target === nodeId && props.id === edge.targetHandle); // only count input edges
                return props.isConnectable({ node, connectedEdges });
            }
            if (typeof props.isConnectable === 'number') {
                const node = nodeInternals.get(nodeId);
                const connectedEdges = (0,reactflow__WEBPACK_IMPORTED_MODULE_2__.getConnectedEdges)([node], edges).filter(edge => edge.target === nodeId && props.id === edge.targetHandle); // only count input edges
                return connectedEdges.length < props.isConnectable;
            }
            return props.isConnectable;
        }, [nodeInternals, edges, nodeId, props.isConnectable, props.id]);
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Handle, { ...props, isConnectable: isHandleConnectable });
    };
    switch (type) {
        case "pandas_df_input":
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Handle, { className: "handle-right", type: "source", position: Position.Right, id: "out" }));
        case "pandas_df_output":
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(LimitedInputHandle, { type: "target", position: Position.Left, isConnectable: 1, className: "handle-left", id: "in" }));
        case "pandas_df_processor":
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(LimitedInputHandle, { type: "target", position: Position.Left, isConnectable: 1, className: "handle-left", id: "in" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Handle, { className: "handle-right", type: "source", position: Position.Right, id: "out" })));
        case "pandas_df_double_processor":
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(LimitedInputHandle, { type: "target", position: Position.Left, isConnectable: 1, className: "handle-left", id: "in1" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(LimitedInputHandle, { type: "target", position: Position.Left, isConnectable: 1, className: "second-handle-left", id: "in2" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Handle, { className: "handle-right", type: "source", position: Position.Right, id: "out" })));
        default:
            return null;
    }
};
const renderComponentUI = ({ id, data, context, manager, commands, name, ConfigForm, Icon, showContent, handle, deleteNode, setViewport }) => {
    const handleDoubleClick = () => {
        // Example: Zoom in 1.2 times the current zoom level
        setViewport({ zoom: 1.2, duration: 500 });
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "component", onDoubleClick: handleDoubleClick },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "component__header" },
                name,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(antd__WEBPACK_IMPORTED_MODULE_1__.Popconfirm, { title: "Sure to delete?", placement: "right", onConfirm: () => deleteNode(), icon: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ant_design_icons__WEBPACK_IMPORTED_MODULE_3__["default"], { style: { color: 'red' } }) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'deletebutton' },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_icons__WEBPACK_IMPORTED_MODULE_4__.xIcon.react, { className: "group-hover:text-primary" })))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "component__body" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("form", null, showContent ? (ConfigForm) : (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "placeholder" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Icon.react, { top: "8px", height: "32px", width: "32px;", color: "#5A8F7B", verticalAlign: "middle" }))))),
            handle)));
};
;


/***/ }),

/***/ "./style/icons/alert-triangle-fill-16.svg":
/*!************************************************!*\
  !*** ./style/icons/alert-triangle-fill-16.svg ***!
  \************************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M8 1a2.143 2.143 0 00-1.827 1.024l-5.88 9.768a2.125 2.125 0 00.762 2.915c.322.188.687.289 1.06.293h11.77a2.143 2.143 0 001.834-1.074 2.126 2.126 0 00-.006-2.124L9.829 2.028A2.149 2.149 0 008 1zM7 11a1 1 0 011-1h.007a1 1 0 110 2H8a1 1 0 01-1-1zm1.75-5.25a.75.75 0 00-1.5 0v2.5a.75.75 0 001.5 0v-2.5z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/crosshair-16.svg":
/*!**************************************!*\
  !*** ./style/icons/crosshair-16.svg ***!
  \**************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M0 8a8 8 0 1116 0A8 8 0 010 8zm8.75 6.457V12.75a.75.75 0 00-1.5 0v1.707A6.503 6.503 0 011.543 8.75H3.25a.75.75 0 000-1.5H1.543A6.503 6.503 0 017.25 1.543V3.25a.75.75 0 001.5 0V1.543a6.503 6.503 0 015.707 5.707H12.75a.75.75 0 000 1.5h1.707a6.503 6.503 0 01-5.707 5.707z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/minus-16.svg":
/*!**********************************!*\
  !*** ./style/icons/minus-16.svg ***!
  \**********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M3.5 7.75A.75.75 0 014.25 7h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/play-16.svg":
/*!*********************************!*\
  !*** ./style/icons/play-16.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M3 3.814C3 2.436 4.52 1.6 5.684 2.334l6.628 4.186a1.75 1.75 0 010 2.96l-6.628 4.185C4.52 14.401 3 13.564 3 12.185v-8.37zm1.883-.211a.25.25 0 00-.383.211v8.372a.25.25 0 00.383.211l6.628-4.186a.25.25 0 000-.422L4.884 3.603z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/play-circle-16.svg":
/*!****************************************!*\
  !*** ./style/icons/play-circle-16.svg ***!
  \****************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\" fill-rule=\"evenodd\" clip-rule=\"evenodd\"><path d=\"M7.421 4.356A1.25 1.25 0 005.5 5.411v5.178a1.25 1.25 0 001.921 1.055l4.069-2.59a1.25 1.25 0 000-2.109L7.42 4.356zM10.353 8L7 10.134V5.866L10.353 8z\"/><path d=\"M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z\"/></g></svg>";

/***/ }),

/***/ "./style/icons/plus-16.svg":
/*!*********************************!*\
  !*** ./style/icons/plus-16.svg ***!
  \*********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" d=\"M9 3.5a.75.75 0 00-1.5 0V7H4a.75.75 0 000 1.5h3.5V12A.75.75 0 009 12V8.5h3.5a.75.75 0 000-1.5H9V3.5z\"/></svg>";

/***/ }),

/***/ "./style/icons/search-16.svg":
/*!***********************************!*\
  !*** ./style/icons/search-16.svg ***!
  \***********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M7.25 2a5.25 5.25 0 103.144 9.455l2.326 2.325a.75.75 0 101.06-1.06l-2.325-2.326A5.25 5.25 0 007.25 2zM3.5 7.25a3.75 3.75 0 117.5 0 3.75 3.75 0 01-7.5 0z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/settings-16.svg":
/*!*************************************!*\
  !*** ./style/icons/settings-16.svg ***!
  \*************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   width=\"16\"\n   height=\"16\"\n   fill=\"none\"\n   viewBox=\"0 0 16 16\"\n   version=\"1.1\"\n   id=\"svg2\"\n   sodipodi:docname=\"settings-16.svg\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <defs\n     id=\"defs2\" />\n  <sodipodi:namedview\n     id=\"namedview2\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:zoom=\"34.875\"\n     inkscape:cx=\"8\"\n     inkscape:cy=\"7.9856631\"\n     inkscape:window-width=\"1392\"\n     inkscape:window-height=\"922\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"75\"\n     inkscape:window-maximized=\"0\"\n     inkscape:current-layer=\"svg2\" />\n  <g\n     fill=\"currentColor\"\n     fill-rule=\"evenodd\"\n     clip-rule=\"evenodd\"\n     id=\"g2\">\n    <path\n       d=\"M8 5a3 3 0 100 6 3 3 0 000-6zM6.5 8a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0z\"\n       id=\"path1\" />\n    <path\n       d=\"M7.5 0a1.75 1.75 0 00-1.75 1.75v.15c-.16.06-.318.125-.472.196l-.106-.106a1.75 1.75 0 00-2.475 0l-.707.707a1.75 1.75 0 000 2.475l.106.106a6.46 6.46 0 00-.196.472h-.15A1.75 1.75 0 000 7.5v1c0 .966.784 1.75 1.75 1.75h.15c.06.16.125.318.196.472l-.106.107a1.75 1.75 0 000 2.474l.707.708a1.75 1.75 0 002.475 0l.106-.107c.154.071.312.137.472.196v.15c0 .966.784 1.75 1.75 1.75h1a1.75 1.75 0 001.75-1.75v-.15c.16-.06.318-.125.472-.196l.106.107a1.75 1.75 0 002.475 0l.707-.707a1.75 1.75 0 000-2.475l-.106-.107c.071-.154.137-.311.196-.472h.15A1.75 1.75 0 0016 8.5v-1a1.75 1.75 0 00-1.75-1.75h-.15a6.455 6.455 0 00-.196-.472l.106-.106a1.75 1.75 0 000-2.475l-.707-.707a1.75 1.75 0 00-2.475 0l-.106.106a6.46 6.46 0 00-.472-.196v-.15A1.75 1.75 0 008.5 0h-1zm-.25 1.75a.25.25 0 01.25-.25h1a.25.25 0 01.25.25v.698c0 .339.227.636.555.724.42.113.817.28 1.186.492a.75.75 0 00.905-.12l.493-.494a.25.25 0 01.354 0l.707.708a.25.25 0 010 .353l-.494.494a.75.75 0 00-.12.904c.213.369.38.767.492 1.186a.75.75 0 00.724.555h.698a.25.25 0 01.25.25v1a.25.25 0 01-.25.25h-.698a.75.75 0 00-.724.555c-.113.42-.28.817-.492 1.186a.75.75 0 00.12.905l.494.493a.25.25 0 010 .354l-.707.707a.25.25 0 01-.354 0l-.494-.494a.75.75 0 00-.904-.12 4.966 4.966 0 01-1.186.492.75.75 0 00-.555.724v.698a.25.25 0 01-.25.25h-1a.25.25 0 01-.25-.25v-.698a.75.75 0 00-.555-.724 4.966 4.966 0 01-1.186-.491.75.75 0 00-.904.12l-.494.493a.25.25 0 01-.354 0l-.707-.707a.25.25 0 010-.354l.494-.493a.75.75 0 00.12-.905 4.966 4.966 0 01-.492-1.186.75.75 0 00-.724-.555H1.75a.25.25 0 01-.25-.25v-1a.25.25 0 01.25-.25h.698a.75.75 0 00.724-.555c.113-.42.28-.817.491-1.186a.75.75 0 00-.12-.904L3.05 4.11a.25.25 0 010-.353l.707-.708a.25.25 0 01.354 0l.493.494c.24.24.611.289.905.12a4.965 4.965 0 011.186-.492.75.75 0 00.555-.724V1.75z\"\n       id=\"path2\" />\n  </g>\n</svg>\n";

/***/ }),

/***/ "./style/icons/trash-16.svg":
/*!**********************************!*\
  !*** ./style/icons/trash-16.svg ***!
  \**********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><g fill=\"currentColor\"><path d=\"M6.25 6a.75.75 0 01.75.75v5.5a.75.75 0 01-1.5 0v-5.5A.75.75 0 016.25 6zM10.5 6.75a.75.75 0 00-1.5 0v5.5a.75.75 0 001.5 0v-5.5z\"/><path fill-rule=\"evenodd\" d=\"M4 3v-.75A2.25 2.25 0 016.25 0h3.5A2.25 2.25 0 0112 2.25V3h2.25a.75.75 0 010 1.5H14v9.25A2.25 2.25 0 0111.75 16h-7.5A2.25 2.25 0 012 13.75V4.5h-.25a.75.75 0 010-1.5H4zm1.5-.75a.75.75 0 01.75-.75h3.5a.75.75 0 01.75.75V3h-5v-.75zm-2 2.25v9.25c0 .414.336.75.75.75h7.5a.75.75 0 00.75-.75V4.5h-9z\" clip-rule=\"evenodd\"/></g></svg>";

/***/ }),

/***/ "./style/icons/x-16.svg":
/*!******************************!*\
  !*** ./style/icons/x-16.svg ***!
  \******************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"16\" height=\"16\" fill=\"none\" viewBox=\"0 0 16 16\"><path fill=\"currentColor\" d=\"M12.78 4.28a.75.75 0 00-1.06-1.06L8 6.94 4.28 3.22a.75.75 0 00-1.06 1.06L6.94 8l-3.72 3.72a.75.75 0 101.06 1.06L8 9.06l3.72 3.72a.75.75 0 101.06-1.06L9.06 8l3.72-3.72z\"/></svg>";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.381da04fdd4f00fefc97.js.map