import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel, Notebook, NotebookActions } from '@jupyterlab/notebook';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ICellModel } from '@jupyterlab/cells';

// Function to handle the event when the notebook content changes
function onNotebookChange(notebook: Notebook): void {
  if (!notebook.model) {
    console.error('Notebook model is null');
    return;
  }
  const notebookJSON = notebook.model.toJSON();
  window.parent.postMessage({
    type: 'notebookChange',
    data: notebookJSON
  }, '*');
}

function onTabChange(notebookPanel: NotebookPanel): void {
  if (!notebookPanel.content.model) {
    console.error('Notebook model is null');
    return;
  }
  const notebookJSON = notebookPanel.content.model.toJSON();
  window.parent.postMessage({
    type: 'tabChange',
    data: notebookJSON
  }, '*');
}

// Function to handle the event when the active cell changes
function onActiveCellChange(notebook: Notebook): void {
  const activeCell = notebook.activeCell;
  const cellData = activeCell?.model.toJSON();
  window.parent.postMessage({
    type: 'activeCellChange',
    data: cellData
  }, '*');
}

// Function to handle changes in any cell's content
function onCellModelChange(cellModel: ICellModel): void {
  const cellData = cellModel.toJSON();
  window.parent.postMessage({
    type: 'cellContentChange',
    data: cellData
  }, '*');
}

// Function to handle cell execution errors
function onCellExecutionError(notebookPanel: NotebookPanel, error: any): void {
  const activeCell = notebookPanel.content.activeCell;
  const cellData = activeCell?.model.toJSON();
  window.parent.postMessage({
    type: 'cellExecutionError',
    data: {
      cellData,
      error: error.message
    }
  }, '*');
}

// Function to add listeners to each cell in the notebook
function addCellListeners(notebook: Notebook): void {
  notebook.widgets.forEach(cell => {
    cell.model.contentChanged.connect(() => onCellModelChange(cell.model));
  });
}

// Function to add the event listeners to a notebook panel
function addChangeListener(notebookPanel: NotebookPanel) {
  // Listen for content changes in the notebook
  notebookPanel.content.modelContentChanged.connect(() => onNotebookChange(notebookPanel.content));
  notebookPanel.content.activeCellChanged.connect(() => onActiveCellChange(notebookPanel.content));

  // Add listeners to each cell for content changes
  addCellListeners(notebookPanel.content);

  if (!notebookPanel?.content?.model) return;
  // Listen for when new cells are added to the notebook
  notebookPanel.content.model.cells.changed.connect(() => {
    addCellListeners(notebookPanel.content);
  });
}


function addCodeToActiveCell(notebook: Notebook, code: string) {
  const activeCell = notebook.activeCell;
  if (activeCell) {
    activeCell.model.sharedModel.setSource(code);
  }
}

function selectOrInsertBelowCell(notebookPanel: NotebookPanel): void {
  if (!notebookPanel || !notebookPanel.content) {
    console.error('Invalid notebook panel');
    return;
  }
  // Save the current active cell index
  const currentActiveCellIndex = notebookPanel.content.activeCellIndex;
  // Try to select the cell below

  const numCells = notebookPanel.model?.cells.length;

  if (numCells && currentActiveCellIndex === numCells - 1) {
    NotebookActions.insertBelow(notebookPanel.content);
  }
  else {
    NotebookActions.selectBelow(notebookPanel.content);
  }
  // Check if the active cell index has changed
}

function selectOrInsertAboveCell(notebookPanel: NotebookPanel): void {
  if (!notebookPanel || !notebookPanel.content) {
    console.error('Invalid notebook panel');
    return;
  }
  // Save the current active cell index
  const currentActiveCellIndex = notebookPanel.content.activeCellIndex;
  // Try to select the cell above
  console.log("current active cell index :", currentActiveCellIndex)
  // if (currentActiveCellIndex === 0) {
  //   NotebookActions.insertAbove(notebookPanel.content);
  // }
  NotebookActions.selectAbove(notebookPanel.content);
  // Check if the active cell index has changed
}


function executeActiveCell(notebookPanel: NotebookPanel) {
  if (!notebookPanel || !notebookPanel.content) {
    console.error('Invalid notebook panel');
    return;
  }
  // Execute the active cell
  NotebookActions.run(notebookPanel.content, notebookPanel.sessionContext).then(
    () => {
      console.log('Cell executed successfully');
    },
    (reason) => {
      console.error('Error executing cell:', reason);
      onCellExecutionError(notebookPanel, reason);
    }
  );
}

function createNewNotebook(documentManager: IDocumentManager, notebookName: string): void {
  // Define the full path for the new notebook
  const path = `${notebookName}.ipynb`;

  // Create a new notebook
  const widget = documentManager.createNew(path, 'notebook');

  if (widget) {
    // Wait for the notebook to be fully loaded
    widget.activate();

  } else {
    console.error('Failed to create a new notebook');
  }
}


function openExistingNotebook(documentManager: IDocumentManager, notebookName: string): void {
  // Define the full path for the notebook
  const path = `${notebookName}.ipynb`;
  const widget = documentManager.openOrReveal(path);
  if (widget) {
    widget.activate()
  }
}

/**
 * Initialization data for the jupyterlab_athena_analytics extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_athena_analytics:plugin',
  autoStart: true,
  requires: [INotebookTracker, IDocumentManager],
  activate: (app: JupyterFrontEnd, tracker: INotebookTracker, docManager: IDocumentManager) => {
    console.log(
      'JupyterLab extension jupyterlab_athena_analytics is activated!'
    );

    // Add change listener to all currently opened notebooks
    tracker.forEach((notebookPanel) => {
      addChangeListener(notebookPanel);
    });

    // Ensure that change listeners are added to new notebooks as they are opened
    tracker.widgetAdded.connect((sender, notebookPanel) => {
      addChangeListener(notebookPanel);
    });

    tracker.currentChanged.connect((sender, notebookPanel) => {
      if (notebookPanel) {
        onTabChange(notebookPanel);
      }
    });

    window.addEventListener('message', (event: MessageEvent) => {
      // Always check the origin for security reasons

      const message = event.data;
      console.log(message);
      const notebookPanel = tracker.currentWidget;

      if (notebookPanel) {
        switch (message.type) {
          case 'selectOrInsertBelowCell':
            selectOrInsertBelowCell(notebookPanel);
            break;
          case 'selectOrInsertAboveCell':
            selectOrInsertAboveCell(notebookPanel);
          case "addCodeToActiveCell":
            addCodeToActiveCell(notebookPanel.content, message.data);
            break;
          case 'executeActiveCell':
            executeActiveCell(notebookPanel);
            break;
          case 'createNewNotebook':
            createNewNotebook(docManager, message.data);
            break;
          case 'openExistingNotebook':
            openExistingNotebook(docManager, message.data);
            break;
          default:
            console.log('Unknown message type:', message.type);
        }
      }
    });


    // Dynamically inject the PostHog analytics script into the document
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.async = true;
    script.innerHTML = `!function(t,e){var o,n,p,r;e._SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e._SV=1)}(document,window.posthog||[]);
    posthog.init('phc_klucwJxuBrgYuAXGSCOUGnp0qhKeA81OuIFyUngiPGQ',{api_host:'https://app.athenaintelligence.ai/ingest', ui_host: 'https://us.posthog.com', session_recording: { recordCrossOriginIframes: true }})`;
    document.head.appendChild(script);
  }
};

export default plugin;
