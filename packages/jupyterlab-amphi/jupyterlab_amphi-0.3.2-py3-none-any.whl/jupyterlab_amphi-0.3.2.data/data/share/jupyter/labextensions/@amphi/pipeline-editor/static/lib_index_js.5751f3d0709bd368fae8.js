"use strict";
(self["webpackChunk_amphi_pipeline_editor"] = self["webpackChunk_amphi_pipeline_editor"] || []).push([["lib_index_js"],{

/***/ "./lib/Dropzone.js":
/*!*************************!*\
  !*** ./lib/Dropzone.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   Dropzone: () => (/* binding */ Dropzone),
/* harmony export */   useDropzone: () => (/* binding */ useDropzone)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

const useDropzone = (props) => {
    const rootRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
    const handleEvent = (0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)((e) => {
        var _a, _b, _c, _d;
        e.preventDefault();
        e.stopPropagation();
        switch (e.type) {
            case 'lm-dragenter':
                (_a = props.onDragEnter) === null || _a === void 0 ? void 0 : _a.call(props, e);
                break;
            case 'lm-dragleave':
                (_b = props.onDragLeave) === null || _b === void 0 ? void 0 : _b.call(props, e);
                break;
            case 'lm-dragover':
                e.dropAction = e.proposedAction;
                (_c = props.onDragOver) === null || _c === void 0 ? void 0 : _c.call(props, e);
                break;
            case 'lm-drop':
                (_d = props.onDrop) === null || _d === void 0 ? void 0 : _d.call(props, e);
                break;
        }
    }, [props]);
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        const node = rootRef.current;
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-dragenter', handleEvent);
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-dragleave', handleEvent);
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-dragover', handleEvent);
        node === null || node === void 0 ? void 0 : node.addEventListener('lm-drop', handleEvent);
        return () => {
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-dragenter', handleEvent);
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-dragleave', handleEvent);
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-dragover', handleEvent);
            node === null || node === void 0 ? void 0 : node.removeEventListener('lm-drop', handleEvent);
        };
    }, [handleEvent]);
    return {
        getRootProps: () => ({
            ref: rootRef,
        }),
    };
};
const Dropzone = ({ children, ...rest }) => {
    const { getRootProps } = useDropzone(rest);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { height: '100%' }, ...getRootProps() }, children));
};


/***/ }),

/***/ "./lib/PipelineEditorWidget.js":
/*!*************************************!*\
  !*** ./lib/PipelineEditorWidget.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FitViewOptions: () => (/* binding */ FitViewOptions),
/* harmony export */   PipelineEditorFactory: () => (/* binding */ PipelineEditorFactory),
/* harmony export */   PipelineEditorWidget: () => (/* binding */ PipelineEditorWidget),
/* harmony export */   commandIDs: () => (/* binding */ commandIDs)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var reactflow__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! reactflow */ "webpack/sharing/consume/default/reactflow/reactflow");
/* harmony import */ var reactflow__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(reactflow__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! antd */ "webpack/sharing/consume/default/antd/antd");
/* harmony import */ var antd__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(antd__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @amphi/pipeline-components-manager */ "webpack/sharing/consume/default/@amphi/pipeline-components-manager");
/* harmony import */ var _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _customEdge__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./customEdge */ "./lib/customEdge.js");
/* harmony import */ var reactflow_dist_style_css__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! reactflow/dist/style.css */ "./node_modules/reactflow/dist/style.css");
/* harmony import */ var _style_output_css__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/output.css */ "./style/output.css");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _Dropzone__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./Dropzone */ "./lib/Dropzone.js");






const { DirectoryTree } = antd__WEBPACK_IMPORTED_MODULE_5__.Tree;






const PIPELINE_CLASS = 'amphi-PipelineEditor';
const commandIDs = {
    openDocManager: 'docmanager:open',
    newDocManager: 'docmanager:new-untitled',
    saveDocManager: 'docmanager:save',
};
const FitViewOptions = {
    padding: 10,
    maxZoom: 1.0
};
/**
 * Initialization: The class extends ReactWidget and initializes the pipeline editor widget. It sets up the initial properties and state for the widget.
 */
class PipelineEditorWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    // Constructor
    constructor(options) {
        super();
        this.browserFactory = options.browserFactory;
        this.defaultFileBrowser = options.defaultFileBrowser;
        this.shell = options.shell;
        this.toolbarRegistry = options.toolbarRegistry;
        this.commands = options.commands;
        this.context = options.context;
        this.settings = options.settings;
        this.componentService = options.componentService;
        let nullPipeline = this.context.model.toJSON() === null;
        this.context.model.contentChanged.connect(() => {
            if (nullPipeline) {
                nullPipeline = false;
                this.update();
            }
        });
    }
    /*
    * Rendering: The render() method is responsible for rendering the widget's UI.
    * It uses various components and elements to display the pipeline editor's interface.
    */
    render() {
        var _a;
        if (this.context.model.toJSON() === null) {
            return react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "amphi-loader" });
        }
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(PipelineWrapper, { context: this.context, browserFactory: this.browserFactory, defaultFileBrowser: this.defaultFileBrowser, shell: this.shell, toolbarRegistry: this.toolbarRegistry, commands: this.commands, widgetId: (_a = this.parent) === null || _a === void 0 ? void 0 : _a.id, settings: this.settings, componentService: this.componentService }));
    }
}
const PipelineWrapper = ({ context, browserFactory, defaultFileBrowser, shell, toolbarRegistry, commands, settings, widgetId, componentService, }) => {
    const manager = defaultFileBrowser.model.manager;
    const edgeTypes = {
        'custom-edge': _customEdge__WEBPACK_IMPORTED_MODULE_9__["default"]
    };
    const nodeTypes = componentService.getComponents().reduce((acc, component) => {
        const id = component._id;
        const ComponentUI = (props) => react__WEBPACK_IMPORTED_MODULE_3___default().createElement(component.UIComponent, { context: context, componentService: componentService, manager: manager, commands: commands, ...props });
        acc[id] = (props) => react__WEBPACK_IMPORTED_MODULE_3___default().createElement(ComponentUI, { context: context, componentService: componentService, manager: manager, commands: commands, ...props });
        return acc;
    }, {});
    const getNodeId = () => `node_${+new Date()}`;
    function PipelineFlow(context) {
        const reactFlowWrapper = (0,react__WEBPACK_IMPORTED_MODULE_3__.useRef)(null);
        const defaultViewport = { x: 0, y: 0, zoom: 1 };
        const [pipeline, setPipeline] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(context.context.model.toJSON());
        const pipelineId = pipeline['id'];
        const initialNodes = pipeline['pipelines'][0]['flow']['nodes'];
        const initialEdges = pipeline['pipelines'][0]['flow']['edges'];
        const [nodes, setNodes, onNodesChange] = (0,reactflow__WEBPACK_IMPORTED_MODULE_4__.useNodesState)(initialNodes);
        const [edges, setEdges, onEdgesChange] = (0,reactflow__WEBPACK_IMPORTED_MODULE_4__.useEdgesState)(initialEdges);
        const [elements, setElements] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)([]); // State for elements
        const [reactFlowInstance, setRfInstance] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(null);
        const { setViewport } = (0,reactflow__WEBPACK_IMPORTED_MODULE_4__.useReactFlow)();
        const updatedPipeline = pipeline;
        updatedPipeline['pipelines'][0]['flow']['nodes'] = nodes;
        updatedPipeline['pipelines'][0]['flow']['edges'] = edges;
        // Save pipeline in current model
        // This means the file can then been save on "disk"
        context.context.model.fromJSON(updatedPipeline);
        const onConnect = (0,react__WEBPACK_IMPORTED_MODULE_3__.useCallback)((params) => setEdges((eds) => (0,reactflow__WEBPACK_IMPORTED_MODULE_4__.addEdge)({ ...params, type: 'custom-edge' }, eds)), [setEdges]);
        /* TODO (edge management)
        const onConnect = (params) => setElements((els) =>
        addEdge({ ...params, type: 'custom-edge' }, els)
        );
        */
        const onNodesDelete = (0,react__WEBPACK_IMPORTED_MODULE_3__.useCallback)((deleted) => {
            setEdges(deleted.reduce((acc, node) => {
                const incomers = (0,reactflow__WEBPACK_IMPORTED_MODULE_4__.getIncomers)(node, nodes, edges);
                const outgoers = (0,reactflow__WEBPACK_IMPORTED_MODULE_4__.getOutgoers)(node, nodes, edges);
                const connectedEdges = (0,reactflow__WEBPACK_IMPORTED_MODULE_4__.getConnectedEdges)([node], edges);
                const remainingEdges = acc.filter((edge) => !connectedEdges.includes(edge));
                const createdEdges = incomers.flatMap(({ id: source }) => outgoers.map(({ id: target }) => ({ id: `${source}->${target}`, source, target, type: 'custom-edge' })));
                return [...remainingEdges, ...createdEdges];
            }, edges));
        }, [nodes, edges]);
        // Manage drag and drop
        const [defaultPosition, setDefaultPosition] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(10);
        const handleAddFileToPipeline = (0,react__WEBPACK_IMPORTED_MODULE_3__.useCallback)((location) => {
            var _a;
            const fileBrowser = defaultFileBrowser;
            // Only add file to pipeline if it is currently in focus
            if (((_a = shell.currentWidget) === null || _a === void 0 ? void 0 : _a.id) !== widgetId) {
                return;
            }
            if (reactFlowInstance && location) {
                const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
                // Adjust the position based on the React Flow instance's coordinate system
                const adjustedPosition = reactFlowInstance.project({
                    x: location.x - reactFlowBounds.left,
                    y: location.y - reactFlowBounds.top,
                });
                Array.from(fileBrowser.selectedItems()).forEach((item) => {
                    const filePath = item.path;
                    const { id: nodeType, default: nodeDefaults } = _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_6__.PipelineService.getComponentIdForFileExtension(item, componentService);
                    // Check if nodeType exists
                    if (nodeType) {
                        const newNode = {
                            id: getNodeId(),
                            type: nodeType,
                            position: adjustedPosition,
                            data: {
                                filePath: filePath,
                                lastUpdated: Date.now(),
                                ...(nodeDefaults || {}) // Merge nodeDefaults into the data field
                            }
                        };
                        // Add the new node to the pipeline
                        setNodes((nds) => nds.concat(newNode));
                    }
                    else {
                        // If nodeType doesn't exist, show the dialog
                        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                            title: 'Unsupported File(s)',
                            body: 'Only supported files (CSV, JSON, PDF, HTML, etc...) can be added to a pipeline.',
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
                        });
                    }
                });
            }
            return;
        }, [defaultFileBrowser, defaultPosition, shell, widgetId, reactFlowInstance]);
        const handleFileDrop = async (e) => {
            handleAddFileToPipeline({ x: e.offsetX, y: e.offsetY });
        };
        const onDragOver = (0,react__WEBPACK_IMPORTED_MODULE_3__.useCallback)((event) => {
            event.preventDefault();
            event.dataTransfer.dropEffect = 'move';
        }, []);
        const onDrop = (0,react__WEBPACK_IMPORTED_MODULE_3__.useCallback)((event) => {
            event.preventDefault();
            const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
            const type = event.dataTransfer.getData('application/reactflow');
            const config = event.dataTransfer.getData('additionalData');
            // check if the dropped element is valid
            if (typeof type === 'undefined' || !type) {
                return;
            }
            const position = reactFlowInstance.project({
                x: event.clientX - reactFlowBounds.left,
                y: event.clientY - reactFlowBounds.top,
            });
            const newNode = {
                id: getNodeId(),
                type,
                position,
                data: {
                    ...config,
                    lastUpdated: Date.now(), // current timestamp in milliseconds
                }
            };
            setNodes((nds) => nds.concat(newNode));
        }, [reactFlowInstance]);
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "reactflow-wrapper", ref: reactFlowWrapper },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_Dropzone__WEBPACK_IMPORTED_MODULE_10__.Dropzone, { onDrop: handleFileDrop },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement((reactflow__WEBPACK_IMPORTED_MODULE_4___default()), { id: pipelineId, nodes: nodes, edges: edges, onNodesChange: onNodesChange, onNodesDelete: onNodesDelete, onEdgesChange: onEdgesChange, onConnect: onConnect, onDrop: onDrop, onDragOver: onDragOver, onInit: setRfInstance, edgeTypes: edgeTypes, nodeTypes: nodeTypes, snapToGrid: true, snapGrid: [15, 15], fitViewOptions: { minZoom: 0.5, maxZoom: 1.0 }, fitView: true, defaultViewport: defaultViewport, deleteKeyCode: [] },
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(reactflow__WEBPACK_IMPORTED_MODULE_4__.Panel, { position: "top-right" }),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(reactflow__WEBPACK_IMPORTED_MODULE_4__.Controls, null),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement(reactflow__WEBPACK_IMPORTED_MODULE_4__.Background, { color: "#aaa", gap: 15 })))));
    }
    function Sidebar() {
        const [sidebarOpen, setSideBarOpen] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(false);
        const sidebarClass = sidebarOpen ? "" : "open";
        const onDragStart = (event, nodeType, config) => {
            event.dataTransfer.setData('application/reactflow', nodeType);
            // Here, you can add more data as needed
            event.dataTransfer.setData('additionalData', config);
            event.dataTransfer.effectAllowed = 'move';
        };
        // Simulating componentService.getComponents()
        const components = componentService.getComponents();
        // Categorizing components with potential subcategories
        const categorizedComponents = {};
        components.forEach(component => {
            let [category, subcategory] = component._category.split('.');
            if (!categorizedComponents[category]) {
                categorizedComponents[category] = {};
            }
            if (subcategory) {
                if (!categorizedComponents[category][subcategory]) {
                    categorizedComponents[category][subcategory] = [];
                }
                categorizedComponents[category][subcategory].push(component);
            }
            else {
                if (!categorizedComponents[category]['_']) { // Maintain a simple placeholder for main categories without explicit subcategories
                    categorizedComponents[category]['_'] = [];
                }
                categorizedComponents[category]['_'].push(component);
            }
        });
        // Transforming categorized components into tree data structure
        const treeData = Object.keys(categorizedComponents).map((category, index) => {
            const subCategories = Object.keys(categorizedComponents[category]);
            let children = [];
            subCategories.forEach((subCat, subIndex) => {
                if (subCat === '_') { // Handling main category direct children
                    children.push(...categorizedComponents[category][subCat].map((component, childIndex) => ({
                        title: (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("span", { draggable: true, className: "palette-component", onDragStart: (event) => onDragStart(event, component._id, component.getDefaultConfig ? component.getDefaultConfig() : ''), key: `category-${index}-item-${childIndex}` }, component._name)),
                        key: `category-${index}-item-${childIndex}`,
                        isLeaf: true,
                        icon: react__WEBPACK_IMPORTED_MODULE_3___default().createElement(component._icon.react, { height: "14px", width: "14px;" })
                    })));
                }
                else { // Handling subcategories
                    children.push({
                        title: react__WEBPACK_IMPORTED_MODULE_3___default().createElement("span", { className: "palette-component-category" }, subCat.charAt(0).toUpperCase() + subCat.slice(1)),
                        key: `category-${index}-sub-${subIndex}`,
                        children: categorizedComponents[category][subCat].map((component, childIndex) => ({
                            title: (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("span", { draggable: true, className: "palette-component", onDragStart: (event) => onDragStart(event, component._id, component.getDefaultConfig ? component.getDefaultConfig() : ''), key: `category-${index}-sub-${subIndex}-item-${childIndex}` }, component._name)),
                            key: `category-${index}-sub-${subIndex}-item-${childIndex}`,
                            isLeaf: true,
                            icon: react__WEBPACK_IMPORTED_MODULE_3___default().createElement(component._icon.react, { height: "14px", width: "14px;" })
                        }))
                    });
                }
            });
            return {
                title: react__WEBPACK_IMPORTED_MODULE_3___default().createElement("span", { className: "palette-component-category" }, category.charAt(0).toUpperCase() + category.slice(1)),
                key: `category-${index}`,
                children: children
            };
        });
        // Output tree data (for debugging, you might want to console.log or use it directly in your components)
        console.log(treeData);
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("aside", { className: sidebarClass, title: 'Components' },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "description" },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.extensionIcon.react, { tag: "span", width: "24px", float: "left", marginRight: "8px" }),
                "Drag and drop components."),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(DirectoryTree, { selectable: false, multiple: true, blockNode: true, defaultExpandAll: true, treeData: treeData, key: "palette-components" })));
    }
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "palette", id: "pipeline-panel" },
        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(reactflow__WEBPACK_IMPORTED_MODULE_4__.ReactFlowProvider, null,
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(PipelineFlow, { context: context }),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement(Sidebar, null))));
};
class PipelineEditorFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    constructor(options) {
        super(options);
        this.browserFactory = options.browserFactory;
        this.defaultFileBrowser = options.defaultFileBrowser;
        this.shell = options.shell;
        this.toolbarRegistry = options.toolbarRegistry;
        this.commands = options.commands;
        this.settings = options.settings;
        this.componentService = options.componentService;
    }
    createNewWidget(context) {
        // Creates a blank widget with a DocumentWidget wrapper
        const props = {
            shell: this.shell,
            toolbarRegistry: this.toolbarRegistry,
            commands: this.commands,
            browserFactory: this.browserFactory,
            defaultFileBrowser: this.defaultFileBrowser,
            context: context,
            settings: this.settings,
            componentService: this.componentService,
        };
        context.sessionContext.kernelPreference = { autoStartDefault: true, name: 'python', shutdownOnDispose: false };
        const content = new PipelineEditorWidget(props);
        const widget = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget({ content, context });
        // Add save button
        // const saveButton = DocToolbarItems.createSaveButton(this.commands, context.fileChanged);
        const saveButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            label: 'Save Pipeline',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.saveIcon,
            onClick: () => {
                this.commands.execute('docmanager:save');
            }
        });
        widget.toolbar.addItem('save', saveButton);
        // Add generate code button
        const generateCodeButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            label: 'Export to Python code',
            iconLabel: 'Export to Python code',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.buildIcon,
            onClick: async () => {
                const code = _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_6__.CodeGenerator.generateCode(context.model.toString(), this.commands, this.componentService);
                // Create a new untitled python file
                const file = await this.commands.execute('docmanager:new-untitled', { path: '/', type: 'file', ext: '.py' }); // TODO, create file in same folder
                // Open the newly created python file
                const doc = await this.commands.execute('docmanager:open', { path: file.path });
                // Set the generated code into the file
                doc.context.model.fromString(code);
            }
        });
        widget.toolbar.addItem('generateCode', generateCodeButton);
        // Add run button
        const runButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            label: 'Run Pipeline',
            iconLabel: 'Run Pipeline',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.runIcon,
            onClick: async () => {
                // First save document
                this.commands.execute('docmanager:save');
                // Second, generate code
                const code = _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_6__.CodeGenerator.generateCode(context.model.toString(), this.commands, this.componentService);
                this.commands.execute('pipeline-editor:run-pipeline', { code }).catch(reason => {
                    console.error(`An error occurred during the execution of 'pipeline-editor:run-pipeline'.\n${reason}`);
                });
            }
        });
        widget.toolbar.addItem('runPipeline', runButton);
        // Add Metadata panel
        const previewPanel = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            label: 'Metadata Panel',
            iconLabel: 'Metadata Panel',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.inspectorIcon,
            onClick: async () => {
                // Call the command execution
                const command = 'metadatapanel:open';
                this.commands.execute(command, {}).catch(reason => {
                    console.error(`An error occurred during the execution of ${command}.\n${reason}`);
                });
            }
        });
        widget.toolbar.addItem('openPreviewPanel', previewPanel);
        // Add Log panel
        const logconsole = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            label: 'Console',
            iconLabel: 'Console',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.listIcon,
            onClick: async () => {
                // Call the command execution
                const command = 'pipeline-console:open';
                this.commands.execute(command, {}).catch(reason => {
                    console.error(`An error occurred during the execution of ${command}.\n${reason}`);
                });
            }
        });
        widget.toolbar.addItem('openlogconsole', logconsole);
        const kernelName = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Toolbar.createKernelNameItem(props.context.sessionContext);
        const spacer = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.Toolbar.createSpacerItem();
        widget.toolbar.addItem('spacer', spacer);
        widget.toolbar.addItem('kernelName', kernelName);
        // add restart runtime button
        /*
        const restartButton = new ToolbarButton({
            label: 'Restart Runtime',
            iconLabel: 'Restart Runtime',
            icon: refreshIcon,
            onClick: async () => {
              // Call the command execution
              const command = 'pipeline-editor:restart-kernel';
              this.commands.execute(command, {}).catch(reason => {
              
              console.error(
                `An error occurred during the execution of ${command}.\n${reason}`
              );
            });
            }
        });
        widget.toolbar.addItem('restartKernel', restartButton);
        */
        widget.addClass(PIPELINE_CLASS);
        widget.title.icon = _icons__WEBPACK_IMPORTED_MODULE_11__.pipelineIcon;
        return widget;
    }
}


/***/ }),

/***/ "./lib/customEdge.js":
/*!***************************!*\
  !*** ./lib/customEdge.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CustomEdge)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var reactflow__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! reactflow */ "webpack/sharing/consume/default/reactflow/reactflow");
/* harmony import */ var reactflow__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(reactflow__WEBPACK_IMPORTED_MODULE_1__);


const onEdgeClick = (evt, id) => {
    evt.stopPropagation();
    alert(`remove ${id}`);
};
function CustomEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, style = {}, markerEnd, }) {
    const { setEdges } = (0,reactflow__WEBPACK_IMPORTED_MODULE_1__.useReactFlow)();
    const [edgePath, labelX, labelY] = (0,reactflow__WEBPACK_IMPORTED_MODULE_1__.getBezierPath)({
        sourceX,
        sourceY,
        sourcePosition,
        targetX,
        targetY,
        targetPosition,
    });
    const onEdgeClick = () => {
        setEdges((edges) => edges.filter((edge) => edge.id !== id));
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(reactflow__WEBPACK_IMPORTED_MODULE_1__.BaseEdge, { path: edgePath, markerEnd: markerEnd, style: style }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(reactflow__WEBPACK_IMPORTED_MODULE_1__.EdgeLabelRenderer, null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: {
                    position: 'absolute',
                    transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
                    fontSize: 12,
                    // everything inside EdgeLabelRenderer has no pointer events by default
                    // if you have an interactive element, set pointer-events: all
                    pointerEvents: 'all',
                }, className: "nodrag nopan" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { className: "edgebutton", onClick: onEdgeClick }, "\u00D7")))));
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   apiIcon: () => (/* binding */ apiIcon),
/* harmony export */   filePlusIcon: () => (/* binding */ filePlusIcon),
/* harmony export */   fileTextIcon: () => (/* binding */ fileTextIcon),
/* harmony export */   monitorIcon: () => (/* binding */ monitorIcon),
/* harmony export */   pipelineBrandIcon: () => (/* binding */ pipelineBrandIcon),
/* harmony export */   pipelineCategoryIcon: () => (/* binding */ pipelineCategoryIcon),
/* harmony export */   pipelineIcon: () => (/* binding */ pipelineIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_icons_file_text_24_svg__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/icons/file-text-24.svg */ "./style/icons/file-text-24.svg");
/* harmony import */ var _style_icons_file_plus_24_svg__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/icons/file-plus-24.svg */ "./style/icons/file-plus-24.svg");
/* harmony import */ var _style_icons_monitor_24_svg__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/icons/monitor-24.svg */ "./style/icons/monitor-24.svg");
/* harmony import */ var _style_icons_api_24_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/icons/api-24.svg */ "./style/icons/api-24.svg");
/* harmony import */ var _style_icons_pipeline_brand_24_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/icons/pipeline-brand-24.svg */ "./style/icons/pipeline-brand-24.svg");
/* harmony import */ var _style_icons_pipeline_brand_16_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/icons/pipeline-brand-16.svg */ "./style/icons/pipeline-brand-16.svg");







const fileTextIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:file-text-icon',
    svgstr: _style_icons_file_text_24_svg__WEBPACK_IMPORTED_MODULE_1__
});
const filePlusIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:file-plus-icon',
    svgstr: _style_icons_file_plus_24_svg__WEBPACK_IMPORTED_MODULE_2__
});
const monitorIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:monitor-icon',
    svgstr: _style_icons_monitor_24_svg__WEBPACK_IMPORTED_MODULE_3__
});
const apiIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:api-icon',
    svgstr: _style_icons_api_24_svg__WEBPACK_IMPORTED_MODULE_4__
});
const pipelineIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipeline-icon',
    svgstr: _style_icons_pipeline_brand_16_svg__WEBPACK_IMPORTED_MODULE_5__
});
const pipelineBrandIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipelinenegative-icon',
    svgstr: _style_icons_pipeline_brand_16_svg__WEBPACK_IMPORTED_MODULE_5__
});
const pipelineCategoryIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'amphi:pipelineCategory-icon',
    svgstr: _style_icons_pipeline_brand_24_svg__WEBPACK_IMPORTED_MODULE_6__
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IPipelineTracker: () => (/* binding */ IPipelineTracker),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @amphi/pipeline-components-manager */ "webpack/sharing/consume/default/@amphi/pipeline-components-manager");
/* harmony import */ var _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _PipelineEditorWidget__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./PipelineEditorWidget */ "./lib/PipelineEditorWidget.js");












/**
 * The command IDs used by the Amphi pipeline editor plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'pipeline-editor:create-new';
    CommandIDs.restartPipelineKernel = 'pipeline-editor:restart-kernel';
    CommandIDs.runPipeline = 'pipeline-editor:run-pipeline';
    CommandIDs.runPipelineUntil = 'pipeline-editor:run-pipeline-until';
})(CommandIDs || (CommandIDs = {}));
const PIPELINE_FACTORY = 'Pipeline Editor';
const PIPELINE = 'amphi-pipeline';
const PIPELINE_EDITOR_NAMESPACE = 'amphi-pipeline-editor';
const PLUGIN_ID = '@amphi/pipeline-editor:extension';
// Export a token so other extensions can require it
const IPipelineTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.Token('pipeline-editor-tracker');
/**
 * Initialization data for the react-widget extension.
 */
const pipelineEditor = {
    id: '@amphi/pipeline-editor:plugin',
    autoStart: true,
    requires: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_6__.IRenderMimeRegistry,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__.IFileBrowserFactory,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__.IDefaultFileBrowser,
        _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__.IStatusBar,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs,
        _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9__.ComponentManager
    ],
    provides: IPipelineTracker,
    activate: (app, palette, rendermime, launcher, browserFactory, defaultFileBrowser, statusBar, restorer, menu, registry, toolbarRegistry, sessionDialogs, componentService) => {
        console.log("Amphi Pipeline Extension activation...");
        // Get app commands and define create-pipeline command
        const { commands } = app;
        const command = CommandIDs.create;
        // Pipeline Tracker
        const pipelineEditortracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: PIPELINE_EDITOR_NAMESPACE
        });
        // Fetch the initial state of the settings.
        const settings = registry.load(PLUGIN_ID).catch(error => console.log(error));
        // Handle state restoration.
        if (restorer) {
            // When restoring the app, if the document was open, reopen it
            restorer.restore(pipelineEditortracker, {
                command: 'docmanager:open',
                args: widget => ({ path: widget.context.path, factory: PIPELINE_FACTORY }),
                name: widget => widget.context.path
            });
        }
        // Set up new widget Factory for .ampln files
        const pipelineEditorFactory = new _PipelineEditorWidget__WEBPACK_IMPORTED_MODULE_10__.PipelineEditorFactory({
            name: PIPELINE_FACTORY,
            fileTypes: [PIPELINE],
            defaultFor: [PIPELINE],
            canStartKernel: true,
            preferKernel: true,
            shutdownOnClose: true,
            shell: app.shell,
            toolbarRegistry: toolbarRegistry,
            commands: app.commands,
            browserFactory: browserFactory,
            defaultFileBrowser: defaultFileBrowser,
            serviceManager: app.serviceManager,
            settings: settings,
            componentService: componentService
        });
        // Add the widget to the tracker when it's created
        pipelineEditorFactory.widgetCreated.connect((sender, widget) => {
            pipelineEditortracker.add(widget);
            // Notify the widget tracker if restore data needs to update
            widget.context.pathChanged.connect(() => {
                pipelineEditortracker.save(widget);
            });
        });
        // Add the default behavior of opening the widget for .ampln files
        // First the Pipeline and then JSON (available)
        app.docRegistry.addFileType({
            name: 'amphi-pipeline',
            displayName: 'pipeline',
            extensions: ['.ampln'],
            icon: _icons__WEBPACK_IMPORTED_MODULE_11__.pipelineBrandIcon,
            fileFormat: 'text'
        }, [PIPELINE_FACTORY, 'JSON']);
        app.docRegistry.addWidgetFactory(pipelineEditorFactory);
        // Add command to create new Pipeline
        commands.addCommand(command, {
            label: args => args['isPalette'] || args['isContextMenu']
                ? 'New Pipeline'
                : 'New Pipeline',
            caption: 'Create a new pipeline',
            icon: (args) => (args['isPalette'] ? null : _icons__WEBPACK_IMPORTED_MODULE_11__.pipelineCategoryIcon),
            execute: async (args) => {
                return commands.execute(_PipelineEditorWidget__WEBPACK_IMPORTED_MODULE_10__.commandIDs.newDocManager, {
                    type: 'file',
                    path: defaultFileBrowser.model.path,
                    ext: '.ampln'
                })
                    .then(async (model) => {
                    const runtime_type = 'LOCAL';
                    const getPipelineId = () => `pipeline_${+new Date()}`;
                    const pipelineJson = {
                        doc_type: 'Amphi Pipeline',
                        version: '1',
                        json_schema: 'http://docs.amphi.ai/schemas/pipeline-v1-schema.json',
                        id: getPipelineId(),
                        pipelines: [
                            {
                                id: 'primary',
                                flow: {
                                    nodes: [],
                                    edges: [],
                                    viewport: {
                                        x: 86,
                                        y: 38,
                                        zoom: 0.5
                                    }
                                },
                                app_data: {
                                    ui_data: {
                                        comments: []
                                    },
                                    version: 1,
                                    runtime_type
                                },
                                runtime_ref: 'python'
                            }
                        ]
                    };
                    // Open Pipeline using Pipeline EditorFactory
                    const newWidget = await app.commands.execute(_PipelineEditorWidget__WEBPACK_IMPORTED_MODULE_10__.commandIDs.openDocManager, {
                        path: model.path,
                        factory: PIPELINE_FACTORY // Use PipelineEditorFactory
                    });
                    // Assign to the new widget context the pipeline JSON from above
                    newWidget.context.ready.then(() => {
                        newWidget.context.model.fromJSON(pipelineJson);
                        // Save this in the file
                        app.commands.execute(_PipelineEditorWidget__WEBPACK_IMPORTED_MODULE_10__.commandIDs.saveDocManager, {
                            path: model.path
                        });
                    });
                });
            }
        });
        // Get the current widget and activate unless the args specify otherwise.
        function getCurrent(args) {
            const widget = pipelineEditortracker.currentWidget;
            const activate = args['activate'] !== false;
            if (activate && widget) {
                app.shell.activateById(widget.id);
            }
            return widget !== null && widget !== void 0 ? widget : null;
        }
        function isEnabled() {
            return (pipelineEditortracker.currentWidget !== null &&
                pipelineEditortracker.currentWidget === app.shell.currentWidget);
        }
        /**
         * Restart the Pipeline Kernel linked to the current Editor
         */
        commands.addCommand(CommandIDs.restartPipelineKernel, {
            label: 'Restart Runtime…',
            execute: async (args) => {
                const current = getCurrent({ activate: false, ...args });
                if (!current) {
                    return;
                }
                console.log(current.context.sessionContext);
                try {
                    await current.context.sessionContext.restartKernel();
                }
                catch (error) {
                    console.error("Failed to restart runtime: ", error);
                }
            },
            isEnabled
        });
        /**
         * Run Pipeline on Kernel linked to the current Editor
         */
        commands.addCommand(CommandIDs.runPipeline, {
            label: 'Run Pipeline',
            execute: args => {
                // Delete Python variables for the metadata panel (reinitialization)
                /*
                const command = 'pipeline-metadata-panel:delete-all';
                commands.execute(command, {}).catch(reason => {
                  console.error(
                    `An error occurred during the execution of ${command}.\n${reason}`
                  );
                });
                */
                // First open log console
                // Open in same panel as metadata panel is openned
                if (args.datapanel) {
                    const command = 'metadatapanel:open';
                    commands.execute(command, {}).catch(reason => {
                        console.error(`An error occurred during the execution of ${command}.\n${reason}`);
                    });
                }
                else {
                    commands.execute('pipeline-console:open', {}).catch(reason => {
                        console.error(`An error occurred during the execution of ${command}.\n${reason}`);
                    });
                }
                const current = getCurrent(args);
                if (!current) {
                    return;
                }
                if (!current.context.sessionContext.session) {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('The pipeline cannot be run because the local Python engine cannot be found.', {
                        actions: [
                            { label: 'Try to reload the application and run again.', callback: () => location.reload() }
                        ],
                        autoClose: 6000
                    });
                    return;
                }
                if (current.context.sessionContext.hasNoKernel) {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('The pipeline cannot be run because no processing engine can be found.', {
                        actions: [
                            { label: 'Try to reload the application and run again.', callback: () => location.reload() }
                        ],
                        autoClose: 6000
                    });
                    return;
                }
                if (!current.context.sessionContext) {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.error('The pipeline cannot be run because the local Python engine cannot be found.', {
                        actions: [
                            { label: 'Try to reload the application and run again.', callback: () => location.reload() }
                        ],
                        autoClose: 6000
                    });
                    return;
                }
                // Second, install dependencies packages if needed
                current.context.sessionContext.ready.then(async () => {
                    const code = args.code.toString();
                    let packages;
                    const imports = _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9__.PipelineService.extractPythonImportPackages(code);
                    packages = _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9__.PipelineService.extractPackageNames(imports);
                    const lines = code.split(/\r?\n/); // Split the code into lines
                    const dependencyLine = lines[2]; // Extract dependencies from the third line (index 2, as arrays are zero-indexed)
                    const dependencies = dependencyLine.startsWith("# Additional dependencies: ") // Assuming the structure is "# Additional imports: package1, package2, ..."
                        ? dependencyLine.split(': ')[1].split(',').map(pkg => pkg.trim())
                        : [];
                    packages = [...packages, ...dependencies];
                    if (packages.length > 0 && packages[0] != null && packages[0] !== '') {
                        const pips_code = _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9__.PipelineService.getInstallCommandsFromPackageNames(packages).join('\n');
                        // Install packages
                        try {
                            const future = current.context.sessionContext.session.kernel.requestExecute({ code: pips_code });
                            future.onReply = reply => {
                                if (reply.content.status == "ok") {
                                    console.log("Dependencies installed successfully");
                                }
                                else if (reply.content.status == "error") {
                                    console.log("Error when installing dependencies");
                                }
                                else if (reply.content.status == "abort") {
                                    console.log("Error when installing dependencies");
                                }
                                else {
                                    console.log("Error when installing dependencies");
                                }
                            };
                            await future.done;
                        }
                        catch (error) {
                            console.error(error);
                        }
                    }
                });
                // Third, run pipeline code
                current.context.sessionContext.ready.then(async () => {
                    try {
                        // Create promise to track success or failure of the request
                        const future = current.context.sessionContext.session.kernel.requestExecute({ code: args.code });
                        future.onReply = reply => {
                            if (reply.content.status == "ok") {
                                console.log("Execution: OK");
                            }
                            else if (reply.content.status == "error") {
                                console.error("Execution: error");
                            }
                            else if (reply.content.status == "abort") {
                                console.log("Execution: abort");
                            }
                            else {
                                console.log("Execution: unknown");
                            }
                        };
                        future.onIOPub = msg => {
                            if (msg.header.msg_type === 'stream') {
                                const streamMsg = msg;
                                // const output = streamMsg.content.text;
                            }
                            else if (msg.header.msg_type === 'error') {
                                // Handle error messages
                                const errorMsg = msg; // If using TypeScript
                                const errorOutput = errorMsg.content; // This contains the error details
                                // Send an error notification with an action button
                                console.error(`Received error: ${errorOutput.ename}: ${errorOutput.evalue}`);
                            }
                        };
                        await future.done;
                    }
                    catch (error) {
                        console.error(error);
                    }
                });
            },
            isEnabled
        });
        commands.addCommand('pipeline-editor:run-pipeline-until', {
            label: 'Run pipeline until ...',
            execute: async (args) => {
                const current = getCurrent(args);
                if (!current) {
                    return;
                }
                const nodeId = args.nodeId.toString();
                const context = args.context;
                const code = _amphi_pipeline_components_manager__WEBPACK_IMPORTED_MODULE_9__.CodeGenerator.generateCodeUntil(current.context.model.toString(), commands, componentService, nodeId, context);
                commands.execute('pipeline-editor:run-pipeline', { code }).catch(reason => {
                    console.error(`An error occurred during the execution of 'pipeline-editor:run-pipeline'.\n${reason}`);
                });
            }
        });
        // Add the command to the context menu
        app.contextMenu.addItem({
            command: CommandIDs.create,
            selector: '.jp-DirListing-content',
            rank: 100,
        });
        // Add to palette
        palette.addItem({
            command: CommandIDs.create,
            category: 'Pipeline',
            args: { isPalette: true }
        });
        /*
        function replaceCategoryIcon(
          category: React.ReactElement,
          icon: LabIcon,
        ): React.ReactElement {
          const children = React.Children.map(category.props.children, (child) => {
            if (child.props.className === 'jp-Launcher-sectionHeader') {
              const grandchildren = React.Children.map(
                child.props.children,
                (grandchild) => {
                  if (grandchild.props.className !== 'jp-Launcher-sectionTitle') {
                    return <icon.react stylesheet="launcherSection" />;
                  } else {
                    return grandchild;
                  }
                },
              );
        
              return React.cloneElement(child, child.props, grandchildren);
            } else {
              return child;
            }
          });
        
          return React.cloneElement(category, category.props, children);
        }
        */
        // Add launcher
        if (launcher) {
            launcher.add({
                command: CommandIDs.create,
                category: 'Amphi',
                rank: 3
            });
        }
        return pipelineEditortracker;
    },
};
/**
 * Export the plugins as default.
 */
const extensions = [
    pipelineEditor
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extensions);


/***/ }),

/***/ "./style/icons/api-24.svg":
/*!********************************!*\
  !*** ./style/icons/api-24.svg ***!
  \********************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M2 5a3 3 0 115.585 1.524l1.79 1.79.68-.68a2.75 2.75 0 013.89 0l.68.68 1.79-1.79a3 3 0 111.06 1.06l-1.79 1.791.681.68a2.75 2.75 0 010 3.89l-.68.68 1.79 1.79a3 3 0 11-1.06 1.06l-1.791-1.79-.68.681a2.75 2.75 0 01-3.89 0l-.68-.68-1.79 1.79a3 3 0 11-1.06-1.06l1.79-1.791-.681-.68a2.75 2.75 0 010-3.89l.68-.68-1.79-1.79A3 3 0 012 5zm3-1.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm0 14a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM17.5 19a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0zM19 3.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm-7.884 5.195a1.25 1.25 0 011.768 0l2.421 2.421a1.25 1.25 0 010 1.768l-2.421 2.421a1.25 1.25 0 01-1.768 0l-2.421-2.421a1.25 1.25 0 010-1.768l2.421-2.421z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/file-plus-24.svg":
/*!**************************************!*\
  !*** ./style/icons/file-plus-24.svg ***!
  \**************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><g fill=\"currentColor\"><path d=\"M11.75 10.75a.75.75 0 01.75.75V14H15a.75.75 0 010 1.5h-2.5V18a.75.75 0 01-1.5 0v-2.5H8.5a.75.75 0 010-1.5H11v-2.5a.75.75 0 01.75-.75z\"/><path fill-rule=\"evenodd\" d=\"M5.75 1A2.75 2.75 0 003 3.75v16.5A2.75 2.75 0 005.75 23h12.5A2.75 2.75 0 0021 20.25V8.664c0-.464-.184-.909-.513-1.237l-5.914-5.914A1.75 1.75 0 0013.336 1H5.75zM4.5 3.75c0-.69.56-1.25 1.25-1.25H13v5.75c0 .414.336.75.75.75h5.75v11.25c0 .69-.56 1.25-1.25 1.25H5.75c-.69 0-1.25-.56-1.25-1.25V3.75zM18.44 7.5L14.5 3.56V7.5h3.94z\" clip-rule=\"evenodd\"/></g></svg>";

/***/ }),

/***/ "./style/icons/file-text-24.svg":
/*!**************************************!*\
  !*** ./style/icons/file-text-24.svg ***!
  \**************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><g fill=\"currentColor\"><path d=\"M7.75 12a.75.75 0 000 1.5h8a.75.75 0 000-1.5h-8zM7 16.75a.75.75 0 01.75-.75h6a.75.75 0 010 1.5h-6a.75.75 0 01-.75-.75zM7.75 8a.75.75 0 000 1.5h2a.75.75 0 000-1.5h-2z\"/><path fill-rule=\"evenodd\" d=\"M3 3.75A2.75 2.75 0 015.75 1h7.586c.464 0 .909.184 1.237.513l5.914 5.914c.329.328.513.773.513 1.237V20.25A2.75 2.75 0 0118.25 23H5.75A2.75 2.75 0 013 20.25V3.75zM5.75 2.5c-.69 0-1.25.56-1.25 1.25v16.5c0 .69.56 1.25 1.25 1.25h12.5c.69 0 1.25-.56 1.25-1.25V9h-5.75a.75.75 0 01-.75-.75V2.5H5.75zm8.75 1.06l3.94 3.94H14.5V3.56z\" clip-rule=\"evenodd\"/></g></svg>";

/***/ }),

/***/ "./style/icons/monitor-24.svg":
/*!************************************!*\
  !*** ./style/icons/monitor-24.svg ***!
  \************************************/
/***/ ((module) => {

module.exports = "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" fill=\"none\" viewBox=\"0 0 24 24\"><path fill=\"currentColor\" fill-rule=\"evenodd\" d=\"M1 4.75A2.75 2.75 0 013.75 2h16.5A2.75 2.75 0 0123 4.75v10.5A2.75 2.75 0 0120.25 18H12.5v2.5H16a.75.75 0 010 1.5H8a.75.75 0 010-1.5h3V18H3.75A2.75 2.75 0 011 15.25V4.75zM20.25 16.5c.69 0 1.25-.56 1.25-1.25V4.75c0-.69-.56-1.25-1.25-1.25H3.75c-.69 0-1.25.56-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h16.5z\" clip-rule=\"evenodd\"/></svg>";

/***/ }),

/***/ "./style/icons/pipeline-brand-16.svg":
/*!*******************************************!*\
  !*** ./style/icons/pipeline-brand-16.svg ***!
  \*******************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   width=\"16\"\n   height=\"16\"\n   fill=\"none\"\n   viewBox=\"0 0 16 16\"\n   version=\"1.1\"\n   id=\"svg1\"\n   sodipodi:docname=\"pipeline-brand-16.svg\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <defs\n     id=\"defs1\" />\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:zoom=\"14.75\"\n     inkscape:cx=\"8\"\n     inkscape:cy=\"7.9661017\"\n     inkscape:window-width=\"1512\"\n     inkscape:window-height=\"874\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"32\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"svg1\" />\n  <path\n     fill=\"currentColor\"\n     fill-rule=\"evenodd\"\n     d=\"M2.75 2.5A1.75 1.75 0 001 4.25v1C1 6.216 1.784 7 2.75 7h1a1.75 1.75 0 001.732-1.5H6.5a.75.75 0 01.75.75v3.5A2.25 2.25 0 009.5 12h1.018c.121.848.85 1.5 1.732 1.5h1A1.75 1.75 0 0015 11.75v-1A1.75 1.75 0 0013.25 9h-1a1.75 1.75 0 00-1.732 1.5H9.5a.75.75 0 01-.75-.75v-3.5A2.25 2.25 0 006.5 4H5.482A1.75 1.75 0 003.75 2.5h-1zM2.5 4.25A.25.25 0 012.75 4h1a.25.25 0 01.25.25v1a.25.25 0 01-.25.25h-1a.25.25 0 01-.25-.25v-1zm9.75 6.25a.25.25 0 00-.25.25v1c0 .138.112.25.25.25h1a.25.25 0 00.25-.25v-1a.25.25 0 00-.25-.25h-1z\"\n     clip-rule=\"evenodd\"\n     id=\"path1\"\n     style=\"fill:#5a8f7b;fill-opacity:1\" />\n</svg>\n";

/***/ }),

/***/ "./style/icons/pipeline-brand-24.svg":
/*!*******************************************!*\
  !*** ./style/icons/pipeline-brand-24.svg ***!
  \*******************************************/
/***/ ((module) => {

module.exports = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n<svg\n   width=\"24\"\n   height=\"24\"\n   fill=\"none\"\n   viewBox=\"0 0 24 24\"\n   version=\"1.1\"\n   id=\"svg1\"\n   sodipodi:docname=\"pipeline-brand-24.svg\"\n   inkscape:version=\"1.3 (0e150ed, 2023-07-21)\"\n   xmlns:inkscape=\"http://www.inkscape.org/namespaces/inkscape\"\n   xmlns:sodipodi=\"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd\"\n   xmlns=\"http://www.w3.org/2000/svg\"\n   xmlns:svg=\"http://www.w3.org/2000/svg\">\n  <defs\n     id=\"defs1\" />\n  <sodipodi:namedview\n     id=\"namedview1\"\n     pagecolor=\"#505050\"\n     bordercolor=\"#eeeeee\"\n     borderopacity=\"1\"\n     inkscape:showpageshadow=\"0\"\n     inkscape:pageopacity=\"0\"\n     inkscape:pagecheckerboard=\"0\"\n     inkscape:deskcolor=\"#505050\"\n     inkscape:zoom=\"9.8333333\"\n     inkscape:cx=\"12\"\n     inkscape:cy=\"11.949153\"\n     inkscape:window-width=\"1512\"\n     inkscape:window-height=\"874\"\n     inkscape:window-x=\"0\"\n     inkscape:window-y=\"32\"\n     inkscape:window-maximized=\"1\"\n     inkscape:current-layer=\"svg1\" />\n  <path\n     fill=\"currentColor\"\n     fill-rule=\"evenodd\"\n     d=\"M4.75 4.5A2.25 2.25 0 002.5 6.75v1A2.25 2.25 0 004.75 10h1a2.25 2.25 0 002.236-2H9.82c.967 0 1.75.784 1.75 1.75v4.5a3.25 3.25 0 003.25 3.25h1.195a2.25 2.25 0 002.236 2h1a2.25 2.25 0 002.25-2.25v-1A2.25 2.25 0 0019.25 14h-1a2.25 2.25 0 00-2.236 2h-1.195a1.75 1.75 0 01-1.75-1.75v-4.5A3.25 3.25 0 009.82 6.5H7.986a2.25 2.25 0 00-2.236-2h-1zM4 6.75A.75.75 0 014.75 6h1a.75.75 0 01.75.75v1a.75.75 0 01-.75.75h-1A.75.75 0 014 7.75v-1zm14.25 8.75a.75.75 0 00-.75.75v1c0 .414.336.75.75.75h1a.75.75 0 00.75-.75v-1a.75.75 0 00-.75-.75h-1z\"\n     clip-rule=\"evenodd\"\n     id=\"path1\"\n     style=\"fill:#5a8f7b;fill-opacity:1\" />\n</svg>\n";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.5751f3d0709bd368fae8.js.map