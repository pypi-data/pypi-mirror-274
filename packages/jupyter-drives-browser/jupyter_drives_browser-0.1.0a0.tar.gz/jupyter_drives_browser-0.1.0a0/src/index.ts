import {
  ILabShell,
  JupyterFrontEndPlugin,
  IRouter,
  JupyterFrontEnd
} from '@jupyterlab/application';
import { showDialog, Dialog } from '@jupyterlab/apputils';
import {
  IDefaultFileBrowser,
  IFileBrowserFactory,
  FileBrowser,
  Uploader
} from '@jupyterlab/filebrowser';

import {
  createToolbarFactory,
  IToolbarWidgetRegistry,
  setToolbar
} from '@jupyterlab/apputils';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { ITranslator } from '@jupyterlab/translation';

import { CommandRegistry } from '@lumino/commands';
import { Widget } from '@lumino/widgets';
import { Drive } from './s3contents';

import { DriveIcon } from './icons';
import { FilenameSearcher, IScore } from '@jupyterlab/ui-components';
import { Token } from '@lumino/coreutils';
import { S3ClientConfig } from '@aws-sdk/client-s3';

/**
 * The command IDs used by the filebrowser plugin.
 */
namespace CommandIDs {
  export const openPath = 'filebrowser:open-path';
  export const openChangeDrive = 'drives:open-change-drive-dialog';
  export const copyToAnotherBucket = 'drives:copy-to-another-bucket';
}

const FILE_BROWSER_FACTORY = 'DriveBrowser';
const FILE_BROWSER_PLUGIN_ID = 'jupyter-drives-browser:file-browser-toolbar';

/**
 * The class name added to the  drive filebrowser filterbox node.
 */
const FILTERBOX_CLASS = 'jp-DriveBrowser-filterBox';

/**
 * The class name added to file dialogs.
 */
const FILE_DIALOG_CLASS = 'jp-FileDialog';

/**
 * The class name added for the new drive label in the switch drive dialog.
 */
const SWITCH_DRIVE_TITLE_CLASS = 'jp-new-drive-title';

/**
 * A promise that resolves to S3 authentication credentials.
 */
export interface IS3Auth {
  factory: () => Promise<{
    bucket: string;
    config: S3ClientConfig;
  }>;
}

/**
 * A token for a plugin that provides S3 authentication.
 */
export const IS3Auth = new Token<IS3Auth>(
  'jupyter-drives-browser:auth-file-browser'
);

/**
 * The auth/credentials provider for the file browser.
 */
const authFileBrowser: JupyterFrontEndPlugin<IS3Auth> = {
  id: 'jupyter-drives-browser:auth-file-browser',
  description: 'The default file browser auth/credentials provider',
  provides: IS3Auth,
  activate: (): IS3Auth => {
    return {
      factory: async () => ({
        bucket: 'jupyter-drives-test-bucket-1',
        config: {
          forcePathStyle: true,
          endpoint: 'https://example.com/s3',
          region: 'eu-west-1',
          credentials: {
            accessKeyId: 'abcdefghijklmnopqrstuvwxyz',
            secretAccessKey: 'SECRET123456789abcdefghijklmnopqrstuvwxyz'
          }
        }
      })
    };
  }
};

/**
 * The default file browser factory provider.
 */
const defaultFileBrowser: JupyterFrontEndPlugin<IDefaultFileBrowser> = {
  id: 'jupyter-drives-browser:default-file-browser',
  description: 'The default file browser factory provider',
  provides: IDefaultFileBrowser,
  requires: [IFileBrowserFactory, IS3Auth],
  optional: [IRouter, JupyterFrontEnd.ITreeResolver, ILabShell],
  activate: async (
    app: JupyterFrontEnd,
    fileBrowserFactory: IFileBrowserFactory,
    s3auth: IS3Auth,
    router: IRouter | null,
    tree: JupyterFrontEnd.ITreeResolver | null,
    labShell: ILabShell | null
  ): Promise<IDefaultFileBrowser> => {
    const { commands } = app;
    const auth = await s3auth.factory();
    // create S3 drive
    const S3Drive = new Drive({ name: auth.bucket, config: auth.config });

    app.serviceManager.contents.addDrive(S3Drive);

    // get registered file types
    S3Drive.getRegisteredFileTypes(app);

    // Manually restore and load the default file browser.
    const defaultBrowser = fileBrowserFactory.createFileBrowser(
      'drivebrowser',
      {
        auto: false,
        restore: false,
        driveName: S3Drive.name
      }
    );

    // TODO: Refactor this.
    // add the filebrowser model to the drive
    S3Drive.fileBrowserModel = defaultBrowser.model;

    Private.addCommands(app, S3Drive, fileBrowserFactory);

    void Private.restoreBrowser(
      defaultBrowser,
      commands,
      router,
      tree,
      labShell
    );

    return defaultBrowser;
  }
};

/**
 * File browser toolbar buttons.
 */
const toolbarFileBrowser: JupyterFrontEndPlugin<void> = {
  id: 'jupyter-drives-browser:file-browser-toolbar',
  description: 'The toolbar for the drives file browser',
  requires: [
    IDefaultFileBrowser,
    IToolbarWidgetRegistry,
    ISettingRegistry,
    ITranslator,
    IFileBrowserFactory
  ],
  autoStart: true,
  activate: async (
    _: JupyterFrontEnd,
    fileBrowser: IDefaultFileBrowser,
    toolbarRegistry: IToolbarWidgetRegistry,
    settingsRegistry: ISettingRegistry,
    translator: ITranslator
  ): Promise<void> => {
    toolbarRegistry.addFactory(
      FILE_BROWSER_FACTORY,
      'uploaderTest',
      (fileBrowser: FileBrowser) =>
        new Uploader({ model: fileBrowser.model, translator })
    );

    toolbarRegistry.addFactory(
      FILE_BROWSER_FACTORY,
      'fileNameSearcherTest',
      (fileBrowser: FileBrowser) => {
        const searcher = FilenameSearcher({
          updateFilter: (
            filterFn: (item: string) => Partial<IScore> | null,
            query?: string
          ) => {
            fileBrowser.model.setFilter(value => {
              return filterFn(value.name.toLowerCase());
            });
          },
          useFuzzyFilter: true,
          placeholder: 'Filter files by namesss',
          forceRefresh: true
        });
        searcher.addClass(FILTERBOX_CLASS);
        return searcher;
      }
    );

    // connect the filebrowser toolbar to the settings registry for the plugin
    setToolbar(
      fileBrowser,
      createToolbarFactory(
        toolbarRegistry,
        settingsRegistry,
        FILE_BROWSER_FACTORY,
        FILE_BROWSER_PLUGIN_ID,
        translator
      )
    );
  }
};

/**
 * Export the plugins as default.
 */
const plugins: JupyterFrontEndPlugin<any>[] = [
  authFileBrowser,
  defaultFileBrowser,
  toolbarFileBrowser
];

export default plugins;

namespace Private {
  /**
   * Create the node for a switch drive handler.
   */
  const createSwitchDriveNode = (oldDriveName: string): HTMLElement => {
    const body = document.createElement('div');
    const existingLabel = document.createElement('label');
    existingLabel.textContent = 'Current Drive';
    const existingName = document.createElement('span');
    existingName.textContent = oldDriveName;

    const nameTitle = document.createElement('label');
    nameTitle.textContent = 'Switch to another Drive';
    nameTitle.className = SWITCH_DRIVE_TITLE_CLASS;
    const name = document.createElement('input');

    body.appendChild(existingLabel);
    body.appendChild(existingName);
    body.appendChild(nameTitle);
    body.appendChild(name);
    return body;
  };

  /**
   * Create the node for a copy to another bucket handler.
   */
  const createCopyToAnotherBucketNode = (): HTMLElement => {
    const body = document.createElement('div');

    const nameTitle = document.createElement('label');
    nameTitle.textContent = 'Copy to another Bucket';
    nameTitle.className = SWITCH_DRIVE_TITLE_CLASS;
    const name = document.createElement('input');

    const location = document.createElement('label');
    location.textContent = 'Location within the Bucket';
    location.className = SWITCH_DRIVE_TITLE_CLASS;
    const locationName = document.createElement('input');

    body.appendChild(nameTitle);
    body.appendChild(name);
    body.appendChild(location);
    body.appendChild(locationName);
    return body;
  };

  /**
   * A widget used to copy files or directories to another bucket.
   */
  export class CopyToAnotherBucket extends Widget {
    /**
     * Construct a new "copy-to-another-bucket" dialog.
     */
    constructor() {
      super({ node: createCopyToAnotherBucketNode() });
      this.onAfterAttach();
    }

    protected onAfterAttach(): void {
      this.addClass(FILE_DIALOG_CLASS);
      const name = this.inputNameNode.value;
      this.inputNameNode.setSelectionRange(0, name.length);
      const location = this.inputLocationNode.value;
      this.inputLocationNode.setSelectionRange(0, location.length);
    }

    /**
     * Get the input text node for the bucket name.
     */
    get inputNameNode(): HTMLInputElement {
      return this.node.getElementsByTagName('input')[0] as HTMLInputElement;
    }

    /**
     * Get the input text node for the location within the bucket.
     */
    get inputLocationNode(): HTMLInputElement {
      return this.node.getElementsByTagName('input')[1] as HTMLInputElement;
    }

    /**
     * Get the value of the widget.
     */
    getValue(): string[] {
      return [this.inputNameNode.value, this.inputLocationNode.value];
    }
  }

  /**
   * A widget used to switch to another drive.
   */
  export class SwitchDriveHandler extends Widget {
    /**
     * Construct a new "switch-drive" dialog.
     */
    constructor(oldDriveName: string) {
      super({ node: createSwitchDriveNode(oldDriveName) });
      this.onAfterAttach();
    }

    protected onAfterAttach(): void {
      this.addClass(FILE_DIALOG_CLASS);
      const value = this.inputNode.value;
      this.inputNode.setSelectionRange(0, value.length);
    }

    /**
     * Get the input text node.
     */
    get inputNode(): HTMLInputElement {
      return this.node.getElementsByTagName('input')[0] as HTMLInputElement;
    }

    /**
     * Get the value of the widget.
     */
    getValue(): string {
      return this.inputNode.value;
    }
  }

  export function addCommands(
    app: JupyterFrontEnd,
    drive: Drive,
    factory: IFileBrowserFactory
  ): void {
    const { tracker } = factory;
    app.commands.addCommand(CommandIDs.openChangeDrive, {
      execute: async () => {
        return showDialog({
          body: new Private.SwitchDriveHandler(drive.name),
          focusNodeSelector: 'input',
          buttons: [
            Dialog.okButton({
              label: 'Switch Drive',
              ariaLabel: 'Switch to another Drive'
            })
          ]
        }).then(result => {
          if (result.value) {
            drive.name = result.value;
            app.serviceManager.contents.addDrive(drive);
          }
        });
      },
      icon: DriveIcon.bindprops({ stylesheet: 'menuItem' })
    });

    app.commands.addCommand(CommandIDs.copyToAnotherBucket, {
      execute: async () => {
        return showDialog({
          body: new Private.CopyToAnotherBucket(),
          focusNodeSelector: 'input',
          buttons: [
            Dialog.okButton({
              label: 'Copy',
              ariaLabel: 'Copy to another Bucket'
            })
          ]
        }).then(result => {
          const widget = tracker.currentWidget;

          if (widget) {
            const path = widget
              .selectedItems()
              .next()!
              .value.path.split(':')[1];

            if (result.value) {
              drive.copyToAnotherBucket(path, result.value[1], result.value[0]);
            }
          }
        });
      },
      icon: DriveIcon.bindprops({ stylesheet: 'menuItem' }),
      label: 'Copy to another Bucket'
    });

    app.contextMenu.addItem({
      command: CommandIDs.copyToAnotherBucket,
      selector:
        '.jp-SidePanel .jp-DirListing-content .jp-DirListing-item[data-isDir]',
      rank: 10
    });
  }

  /**
   * Restores file browser state and overrides state if tree resolver resolves.
   */
  export async function restoreBrowser(
    browser: FileBrowser,
    commands: CommandRegistry,
    router: IRouter | null,
    tree: JupyterFrontEnd.ITreeResolver | null,
    labShell: ILabShell | null
  ): Promise<void> {
    const restoring = 'jp-mod-restoring';

    browser.addClass(restoring);

    if (!router) {
      await browser.model.restore(browser.id);
      await browser.model.refresh();
      browser.removeClass(restoring);
      return;
    }

    const listener = async () => {
      router.routed.disconnect(listener);

      const paths = await tree?.paths;
      if (paths?.file || paths?.browser) {
        // Restore the model without populating it.
        await browser.model.restore(browser.id, false);
        if (paths.file) {
          await commands.execute(CommandIDs.openPath, {
            path: paths.file,
            dontShowBrowser: true
          });
        }
        if (paths.browser) {
          await commands.execute(CommandIDs.openPath, {
            path: paths.browser,
            dontShowBrowser: true
          });
        }
      } else {
        await browser.model.restore(browser.id);
        await browser.model.refresh();
      }
      browser.removeClass(restoring);

      if (labShell?.isEmpty('main')) {
        void commands.execute('launcher:create');
      }
    };
    router.routed.connect(listener);
  }
}
