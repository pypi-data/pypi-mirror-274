import { Signal, ISignal } from '@lumino/signaling';
import { Contents, ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { FileBrowserModel } from '@jupyterlab/filebrowser';

import {
  CopyObjectCommand,
  DeleteObjectCommand,
  S3Client,
  ListObjectsV2Command,
  GetBucketLocationCommand,
  GetObjectCommand,
  PutObjectCommand,
  HeadObjectCommand,
  S3ClientConfig
} from '@aws-sdk/client-s3';

import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

let data: Contents.IModel = {
  name: '',
  path: '',
  last_modified: '',
  created: '',
  content: null,
  format: null,
  mimetype: '',
  size: 0,
  writable: true,
  type: ''
};

export interface IRegisteredFileTypes {
  [fileExtension: string]: {
    fileType: string;
    fileMimeTypes: string[];
    fileFormat: string;
  };
}

export class Drive implements Contents.IDrive {
  /**
   * Construct a new drive object.
   *
   * @param options - The options used to initialize the object.
   */
  constructor(options: Drive.IOptions) {
    this._serverSettings = ServerConnection.makeSettings();

    this._s3Client = new S3Client(options.config ?? {});
    this._name = options.name;
    this._baseUrl = URLExt.join(
      (options.config?.endpoint as string) ?? 'https://s3.amazonaws.com/',
      this._name
    );
    this._provider = 'S3';

    this.getRegion().then((region: string) => {
      this._region = region!;
    });

    this._registeredFileTypes = {};
  }

  /**
   * The Drive S3 client
   */
  get s3Client(): S3Client {
    return this._s3Client;
  }

  /**
   * The Drive S3 client
   */
  set s3Client(s3Client: S3Client) {
    this._s3Client = s3Client;
  }

  /**
   * The Drive base URL
   */
  get baseUrl(): string {
    return this._baseUrl;
  }

  /**
   * The Drive base URL
   */
  set baseUrl(url: string) {
    this._baseUrl = url;
  }

  /**
   * The Drive name getter
   */
  get name(): string {
    return this._name;
  }

  /**
   * The Drive name setter */
  set name(name: string) {
    this._name = name;
  }

  /**
   * The Drive provider getter
   */
  get provider(): string {
    return this._provider;
  }

  /**
   * The Drive provider setter */
  set provider(name: string) {
    this._provider = name;
  }

  /**
   * The Drive region getter
   */
  get region(): string {
    return this._region;
  }

  /**
   * The Drive region setter
   */
  set region(region: string) {
    this._region = region;
  }

  /**
   * The Drive creationDate getter
   */
  get creationDate(): string {
    return this._creationDate;
  }

  /**
   * The Drive creationDate setter
   */
  set creationDate(date: string) {
    this._creationDate = date;
  }

  /**
   * The registered file types
   */
  get registeredFileTypes(): IRegisteredFileTypes {
    return this._registeredFileTypes;
  }

  /**
   * The registered file types
   */
  set registeredFileTypes(fileTypes: IRegisteredFileTypes) {
    this._registeredFileTypes = fileTypes;
  }

  /**
   * Settings for the notebook server.
   */
  get serverSettings(): ServerConnection.ISettings {
    return this._serverSettings;
  }

  /**
   * A signal emitted when a file operation takes place.
   */
  get fileChanged(): ISignal<this, Contents.IChangedArgs> {
    return this._fileChanged;
  }

  /**
   * Test whether the manager has been disposed.
   */
  get isDisposed(): boolean {
    return this._isDisposed;
  }

  /**
   * A signal emitted when the drive is disposed.
   */
  get disposed(): ISignal<this, void> {
    return this._disposed;
  }

  /**
   * Set the filebrowser model connected to the drive.
   */
  set fileBrowserModel(fileBrowserModel: FileBrowserModel) {
    this._fileBrowserModel = fileBrowserModel;
  }

  /**
   * Get the filebrowser model connected to the drive.
   */
  get fileBrowserModel(): FileBrowserModel {
    return this._fileBrowserModel!;
  }

  /**
   * Dispose of the resources held by the manager.
   */
  dispose(): void {
    if (this.isDisposed) {
      return;
    }
    this._isDisposed = true;
    this._disposed.emit();
    Signal.clearData(this);
  }

  /**
   * Get an encoded download url given a file path.
   *
   * @param path - An absolute POSIX file path on the server.
   *
   * #### Notes
   * It is expected that the path contains no relative paths,
   * use [[ContentsManager.getAbsolutePath]] to get an absolute
   * path if necessary.
   */
  async getDownloadUrl(path: string): Promise<string> {
    const getCommand = new GetObjectCommand({
      Bucket: this._name,
      Key: path,
      ResponseContentDisposition: 'attachment',
      ResponseContentType: 'application/octet-stream'
    });

    await this._s3Client.send(getCommand);

    // get pre-signed URL of S3 file
    const signedUrl = await getSignedUrl(this._s3Client, getCommand);
    return signedUrl;
  }

  /**
   * Get a file or directory.
   *
   * @param localPath: The path to the file.
   *
   * @param options: The options used to fetch the file.
   *
   * @returns A promise which resolves with the file content.
   *
   * Uses the [Jupyter Notebook API](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter-server/jupyter_server/main/jupyter_server/services/api/api.yaml#!/contents) and validates the response model.
   */
  async get(
    path: string,
    options?: Contents.IFetchOptions
  ): Promise<Contents.IModel> {
    path = path.replace(this._name + '/', '');

    // check if we are getting the list of files from the drive
    if (!path) {
      const content: Contents.IModel[] = [];

      const command = new ListObjectsV2Command({
        Bucket: this._name
      });

      let isTruncated: boolean | undefined = true;

      while (isTruncated) {
        const { Contents, IsTruncated, NextContinuationToken } =
          await this._s3Client.send(command);

        if (Contents) {
          Contents.forEach(c => {
            // checking if we are dealing with the file inside a folder
            if (c.Key!.split('/').length === 1 || c.Key!.split('/')[1] === '') {
              const [fileType, fileMimeType, fileFormat] = this.getFileType(
                c.Key!.split('.')[1]
              );

              content.push({
                name: !c.Key!.split('.')[1] ? c.Key!.slice(0, -1) : c.Key!,
                path: c.Key!,
                last_modified: c.LastModified!.toISOString(),
                created: '',
                content: !c.Key!.split('.')[1] ? [] : null,
                format: fileFormat as Contents.FileFormat,
                mimetype: fileMimeType,
                size: c.Size!,
                writable: true,
                type: fileType
              });
            }
          });
        }
        if (isTruncated) {
          isTruncated = IsTruncated;
        }
        command.input.ContinuationToken = NextContinuationToken;
      }

      data = {
        name: this._name,
        path: this._name,
        last_modified: '',
        created: '',
        content: content,
        format: 'json',
        mimetype: '',
        size: undefined,
        writable: true,
        type: 'directory'
      };
    } else {
      const splitPath = path.split('/');
      const currentPath = splitPath[splitPath.length - 1];

      // listing contents of a folder
      if (currentPath.indexOf('.') === -1) {
        const content: Contents.IModel[] = [];

        const command = new ListObjectsV2Command({
          Bucket: this._name,
          Prefix: currentPath + '/'
        });

        let isTruncated: boolean | undefined = true;

        while (isTruncated) {
          const { Contents, IsTruncated, NextContinuationToken } =
            await this._s3Client.send(command);

          if (Contents) {
            Contents.forEach(c => {
              // checking if we are dealing with the file inside a folder
              if (c.Key !== currentPath + '/') {
                const fileName = c.Key!.split('/')[1];
                const [fileType, fileMimeType, fileFormat] = this.getFileType(
                  c.Key!.split('.')[1]
                );

                content.push({
                  name: fileName,
                  path: path + '/' + fileName,
                  last_modified: c.LastModified!.toISOString(),
                  created: '',
                  content: !c.Key!.split('.')[1] ? [] : null,
                  format: fileFormat as Contents.FileFormat,
                  mimetype: fileMimeType,
                  size: c.Size!,
                  writable: true,
                  type: fileType
                });
              }
            });
          }
          if (isTruncated) {
            isTruncated = IsTruncated;
          }
          command.input.ContinuationToken = NextContinuationToken;
        }

        data = {
          name: currentPath,
          path: path + '/',
          last_modified: '',
          created: '',
          content: content,
          format: 'json',
          mimetype: '',
          size: undefined,
          writable: true,
          type: 'directory'
        };
      }
      // getting the contents of a specific file
      else {
        const command = new GetObjectCommand({
          Bucket: this._name,
          Key: path.replace(this._name + '/', '')
        });

        const response = await this._s3Client.send(command);

        if (response) {
          const date: string = response.LastModified!.toISOString();
          const [fileType, fileMimeType, fileFormat] = this.getFileType(
            currentPath.split('.')[1]
          );

          let fileContents: string | Uint8Array;

          // for certain media type files, extract content as byte array and decode to base64 to view in JupyterLab
          if (fileFormat === 'base64' || fileType === 'PDF') {
            fileContents = await response.Body!.transformToByteArray();
            fileContents = btoa(
              fileContents.reduce(
                (data, byte) => data + String.fromCharCode(byte),
                ''
              )
            );
          } else {
            fileContents = await response.Body!.transformToString();
          }

          data = {
            name: currentPath,
            path: path,
            last_modified: date,
            created: '',
            content: fileContents,
            format: fileFormat as Contents.FileFormat,
            mimetype: fileMimeType,
            size: response.ContentLength!,
            writable: true,
            type: fileType
          };
        }
      }
    }

    Contents.validateContentsModel(data);
    return data;
  }

  /**
   * Create a new untitled file or directory in the specified directory path.
   *
   * @param options: The options used to create the file.
   *
   * @returns A promise which resolves with the created file content when the
   *    file is created.
   */
  async newUntitled(
    options: Contents.ICreateOptions = {}
  ): Promise<Contents.IModel> {
    const body = '';

    // get current list of contents of drive
    const content: Contents.IModel[] = [];

    const command = new ListObjectsV2Command({
      Bucket: this._name
    });

    let isTruncated: boolean | undefined = true;

    while (isTruncated) {
      const { Contents, IsTruncated, NextContinuationToken } =
        await this._s3Client.send(command);

      if (Contents) {
        Contents.forEach(c => {
          const [fileType, fileMimeType, fileFormat] = this.getFileType(
            c.Key!.split('.')[1]
          );

          content.push({
            name: c.Key!,
            path: URLExt.join(this._name, c.Key!),
            last_modified: c.LastModified!.toISOString(),
            created: '',
            content: !c.Key!.split('.')[1] ? [] : null,
            format: fileFormat as Contents.FileFormat,
            mimetype: fileMimeType,
            size: c.Size!,
            writable: true,
            type: fileType
          });
        });
      }
      if (isTruncated) {
        isTruncated = IsTruncated;
      }
      command.input.ContinuationToken = NextContinuationToken;
    }

    const old_data: Contents.IModel = {
      name: this._name,
      path: '',
      last_modified: '',
      created: '',
      content: content,
      format: 'json',
      mimetype: '',
      size: undefined,
      writable: true,
      type: 'directory'
    };

    if (options.type !== undefined) {
      if (options.type !== 'directory') {
        const name = this.incrementUntitledName(old_data, options);
        await this.s3Client.send(
          new PutObjectCommand({
            Bucket: this._name,
            Key: options.path ? options.path + '/' + name : name,
            Body: body
          })
        );

        const [fileType, fileMimeType, fileFormat] = this.getFileType(
          options.ext!
        );

        data = {
          name: name,
          path: options.path + '/' + name,
          last_modified: new Date().toISOString(),
          created: new Date().toISOString(),
          content: body,
          format: fileFormat as Contents.FileFormat,
          mimetype: fileMimeType,
          size: body.length,
          writable: true,
          type: fileType
        };
      } else {
        // creating a new directory
        const name = this.incrementUntitledName(old_data, options);
        await this.s3Client.send(
          new PutObjectCommand({
            Bucket: this._name,
            Key: options.path ? options.path + '/' + name + '/' : name + '/',
            Body: body
          })
        );

        data = {
          name: name,
          path: options.path + '/' + name,
          last_modified: new Date().toISOString(),
          created: new Date().toISOString(),
          content: [],
          format: 'json',
          mimetype: 'text/directory',
          size: undefined,
          writable: true,
          type: options.type
        };
      }
    } else {
      console.warn('Type of new element is undefined');
    }

    // manually refresh filebrowser contents
    this._fileBrowserModel!.refresh();

    Contents.validateContentsModel(data);
    this._fileChanged.emit({
      type: 'new',
      oldValue: null,
      newValue: data
    });

    return data;
  }

  incrementUntitledName(
    contents: Contents.IModel,
    options: Contents.ICreateOptions
  ): string {
    const content: Array<Contents.IModel> = contents.content;
    let name: string = '';
    let countText = 0;
    let countDir = 0;
    let countNotebook = 0;
    if (options.type === 'notebook') {
      options.ext = 'ipynb';
    }

    content.forEach(item => {
      if (options.ext !== undefined) {
        if (item.name.includes('untitled') && item.name.includes('.txt')) {
          countText = countText + 1;
        } else if (
          item.name.includes('Untitled') &&
          item.name.includes('.ipynb')
        ) {
          countNotebook = countNotebook + 1;
        }
      } else if (item.name.includes('Untitled Folder')) {
        countDir = countDir + 1;
      }
    });

    if (options.ext === 'txt') {
      if (countText === 0) {
        name = 'untitled' + '.' + options.ext;
      } else {
        name = 'untitled' + countText + '.' + options.ext;
      }
    }
    if (options.ext === 'ipynb') {
      if (countNotebook === 0) {
        name = 'Untitled' + '.' + options.ext;
      } else {
        name = 'Untitled' + countNotebook + '.' + options.ext;
      }
    } else if (options.type === 'directory') {
      if (countDir === 0) {
        name = 'Untitled Folder';
      } else {
        name = 'Untitled Folder ' + countDir;
      }
    }
    return name;
  }

  /**
   * Delete a file.
   *
   * @param path - The path to the file.
   *
   * @returns A promise which resolves when the file is deleted.
   */
  async delete(localPath: string): Promise<void> {
    // check if we are dealing with a directory
    const info = await this.s3Client.send(
      new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: localPath
      })
    );

    let isDir = 0;
    if (
      info.Contents!.length > 1 ||
      info.Contents![0].Key![info.Contents![0].Key!.length - 1] === '/'
    ) {
      localPath = localPath + '/';
      isDir = 1;
    }

    await this.s3Client.send(
      new DeleteObjectCommand({
        Bucket: this._name,
        Key: localPath
      })
    );

    // if we are dealing with a directory, delete the files inside it
    if (isDir) {
      // get list of content from deleted directory
      const command = new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: localPath
      });

      let isTruncated: boolean | undefined = true;

      while (isTruncated) {
        const { Contents, IsTruncated, NextContinuationToken } =
          await this._s3Client.send(command);

        if (Contents) {
          Contents.forEach(c => {
            this.delete_file(c.Key!);
          });
        }
        if (isTruncated) {
          isTruncated = IsTruncated;
        }
        command.input.ContinuationToken = NextContinuationToken;
      }
    }

    // manually refresh filebrowser contents
    this._fileBrowserModel!.refresh();

    this._fileChanged.emit({
      type: 'delete',
      oldValue: { path: localPath },
      newValue: { path: undefined }
    });
  }

  /**
   * Rename a file or directory.
   *
   * @param oldLocalPath - The original file path.
   *
   * @param newLocalPath - The new file path.
   *
   * @returns A promise which resolves with the new file contents model when
   *   the file is renamed.
   *
   * #### Notes
   * Uses the [Jupyter Notebook API](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter-server/jupyter_server/main/jupyter_server/services/api/api.yaml#!/contents) and validates the response model.
   */
  async rename(
    oldLocalPath: string,
    newLocalPath: string,
    options: Contents.ICreateOptions = {}
  ): Promise<Contents.IModel> {
    let newFileName =
      newLocalPath.indexOf('/') >= 0
        ? newLocalPath.split('/')[newLocalPath.split('/').length - 1]
        : newLocalPath;

    // check if we are dealing with a directory
    const info = await this.s3Client.send(
      new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: oldLocalPath
      })
    );

    let isDir: boolean = false;
    if (
      info.Contents!.length > 1 ||
      info.Contents![0].Key![info.Contents![0].Key!.length - 1] === '/'
    ) {
      oldLocalPath = oldLocalPath + '/';
      newLocalPath = newLocalPath + '/';
      isDir = true;
    }

    // retrieve information of old file
    const fileContents = await this._s3Client.send(
      new GetObjectCommand({
        Bucket: this._name,
        Key: oldLocalPath
      })
    );

    // delete old object
    await this._s3Client.send(
      new DeleteObjectCommand({
        Bucket: this._name,
        Key: oldLocalPath
      })
    );

    // check if file with new name already exists
    try {
      await this._s3Client.send(
        new HeadObjectCommand({
          Bucket: this._name,
          Key: newLocalPath
        })
      );
      console.log('File name already exists!');
      // construct new incremented name and it's corresponding path
      newFileName = await this.incrementName(newLocalPath, isDir, this._name);
      if (isDir) {
        newLocalPath = newLocalPath.substring(0, newLocalPath.length - 1);
      }
      newLocalPath = isDir
        ? newLocalPath.substring(0, newLocalPath.lastIndexOf('/') + 1) +
          newFileName +
          '/'
        : newLocalPath.substring(0, newLocalPath.lastIndexOf('/') + 1) +
          newFileName;
    } catch (e) {
      // function throws error as the file name doesn't exist
      console.log("Name doesn't exist!");
    }

    const body = await fileContents.Body?.transformToString();

    // create new file with same content, but different name
    await this.s3Client.send(
      new PutObjectCommand({
        Bucket: this._name,
        Key: newLocalPath,
        Body: body
      })
    );

    // in the case of renaming a directory, move files to new location
    if (isDir) {
      // get list of content from old directory
      const command = new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: oldLocalPath
      });

      let isTruncated: boolean | undefined = true;

      while (isTruncated) {
        const { Contents, IsTruncated, NextContinuationToken } =
          await this._s3Client.send(command);

        if (Contents) {
          Contents.forEach(c => {
            const fileName = c.Key!.split('/')[c.Key!.split.length - 1];
            this.copy_file(fileName, oldLocalPath, newLocalPath, this._name);
          });
        }
        if (isTruncated) {
          isTruncated = IsTruncated;
        }
        command.input.ContinuationToken = NextContinuationToken;
      }
    }
    const [fileType, fileMimeType, fileFormat] = this.getFileType(
      newFileName!.split('.')[1]
    );

    const data = {
      name: newFileName,
      path: newLocalPath,
      last_modified: fileContents.LastModified!.toISOString(),
      created: '',
      content: isDir ? [] : body,
      format: fileFormat as Contents.FileFormat,
      mimetype: fileMimeType,
      size: fileContents.ContentLength!,
      writable: true,
      type: fileType
    };

    // manually refresh filebrowser contents
    this._fileBrowserModel!.refresh();

    this._fileChanged.emit({
      type: 'rename',
      oldValue: { path: oldLocalPath },
      newValue: data
    });
    Contents.validateContentsModel(data);
    return data;
  }

  /**
   * Helping function to increment name of existing files or directorties.
   *
   * @param localPath - Path to file.
   *
   * @param isDir - Whether the content is a directory or a file.
   *
   * @param bucketName - The name of the bucket where content is moved.
   */
  async incrementName(localPath: string, isDir: boolean, bucketName: string) {
    let counter: number = 0;
    let fileExtension: string = '';
    let originalName: string = '';

    // check if we are dealing with a directory
    if (isDir) {
      localPath = localPath.substring(0, localPath.length - 1);
      originalName = localPath.split('/')[localPath.split('/').length - 1];
    }
    // dealing with a file
    else {
      // extract name from path
      originalName = localPath.split('/')[localPath.split('/').length - 1];
      // eliminate file extension
      fileExtension =
        originalName.split('.')[originalName.split('.').length - 1];
      originalName =
        originalName.split('.')[originalName.split('.').length - 2];
    }

    // count number of name appearances
    const command = new ListObjectsV2Command({
      Bucket: bucketName,
      Prefix: localPath.substring(0, localPath.lastIndexOf('/'))
    });

    let isTruncated: boolean | undefined = true;

    while (isTruncated) {
      const { Contents, IsTruncated, NextContinuationToken } =
        await this._s3Client.send(command);

      if (Contents) {
        Contents.forEach(c => {
          // check if we are dealing with a directory
          if (c.Key![c.Key!.length - 1] === '/') {
            c.Key! = c.Key!.substring(0, c.Key!.length - 1);
          }
          // check if the name of the file or directory matches the original name
          if (
            c
              .Key!.substring(
                c.Key!.lastIndexOf('/') + 1,
                c.Key!.lastIndexOf('/') + 1 + originalName.length
              )
              .includes(originalName)
          ) {
            counter += 1;
          }
        });
      }
      if (isTruncated) {
        isTruncated = IsTruncated;
      }
      command.input.ContinuationToken = NextContinuationToken;
    }

    let newName = counter ? originalName + counter : originalName;
    newName = isDir ? newName + '/' : newName + '.' + fileExtension;

    return newName;
  }

  /**
   * Save a file.
   *
   * @param localPath - The desired file path.
   *
   * @param options - Optional overrides to the model.
   *
   * @returns A promise which resolves with the file content model when the
   *   file is saved.
   *
   * #### Notes
   * Ensure that `model.content` is populated for the file.
   *
   * Uses the [Jupyter Notebook API](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter-server/jupyter_server/main/jupyter_server/services/api/api.yaml#!/contents) and validates the response model.
   */
  async save(
    localPath: string,
    options: Partial<Contents.IModel> = {}
  ): Promise<Contents.IModel> {
    const fileName =
      localPath.indexOf('/') === -1
        ? localPath
        : localPath.split('/')[localPath.split.length - 1];

    const [fileType, fileMimeType, fileFormat] = this.getFileType(
      fileName.split('.')[1]
    );

    let body: string | Blob;
    if (options.format === 'json') {
      body = JSON.stringify(options?.content, null, 2);
    } else if (
      options.format === 'base64' &&
      (fileFormat === 'base64' || fileType === 'PDF')
    ) {
      // transform base64 encoding to a utf-8 array for saving and storing in S3 bucket
      const byteCharacters = atob(options.content);
      const byteArrays = [];

      for (let offset = 0; offset < byteCharacters.length; offset += 512) {
        const slice = byteCharacters.slice(offset, offset + 512);
        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }

      body = new Blob(byteArrays, { type: fileMimeType });
    } else {
      body = options?.content;
    }

    // save file with new content by overwritting existing file
    await this._s3Client.send(
      new PutObjectCommand({
        Bucket: this._name,
        Key: localPath,
        Body: body,
        CacheControl: 'no-cache'
      })
    );

    data = {
      name: fileName,
      path: localPath,
      last_modified: new Date().toISOString(),
      created: '',
      content: body,
      format: fileFormat as Contents.FileFormat,
      mimetype: fileMimeType,
      size: typeof body === 'string' ? body.length : body.size,
      writable: true,
      type: fileType
    };

    // manually refresh filebrowser contents
    this._fileBrowserModel!.refresh();

    this._fileChanged.emit({
      type: 'save',
      oldValue: null,
      newValue: data
    });
    Contents.validateContentsModel(data);
    return data;
  }

  /**
   * Copy a file into a given directory.
   *
   * @param path - The original file path.
   *
   * @param isDir - The boolean marking if we are dealing with a file or directory.
   *
   * @param bucketName - The name of the bucket where content is moved.
   *
   * @returns A promise which resolves with the new name when the
   *  file is copied.
   */
  async incrementCopyName(
    copiedItemPath: string,
    isDir: boolean,
    bucketName: string
  ) {
    // extracting original file name
    const originalFileName =
      copiedItemPath.split('/')[copiedItemPath.split('/').length - 1];

    // constructing new file name and path with -Copy string
    const newFileName = isDir
      ? originalFileName + '-Copy'
      : originalFileName.split('.')[0] +
        '-Copy.' +
        originalFileName.split('.')[1];

    const newFilePath = isDir
      ? copiedItemPath.substring(0, copiedItemPath.lastIndexOf('/') + 1) +
        newFileName +
        '/'
      : copiedItemPath.substring(0, copiedItemPath.lastIndexOf('/') + 1) +
        newFileName;

    // getting incremented name of Copy in case of duplicates
    const incrementedName = await this.incrementName(
      newFilePath,
      isDir,
      bucketName
    );

    return incrementedName;
  }

  /**
   * Copy a file into a given directory.
   *
   * @param path - The original file path.
   *
   * @param toDir - The destination directory path.
   *
   * @returns A promise which resolves with the new contents model when the
   *  file is copied.
   */
  async copy(
    path: string,
    toDir: string,
    options: Contents.ICreateOptions = {}
  ): Promise<Contents.IModel> {
    // check if we are dealing with a directory
    const info = await this.s3Client.send(
      new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: path
      })
    );

    let isDir: boolean = false;
    if (
      info.Contents!.length > 1 ||
      info.Contents![0].Key![info.Contents![0].Key!.length - 1] === '/'
    ) {
      isDir = true;
    }

    // construct new file or directory name for the copy
    const newFileName = await this.incrementCopyName(path, isDir, this._name);
    path = isDir ? path + '/' : path;

    await this._s3Client.send(
      new CopyObjectCommand({
        Bucket: this._name,
        CopySource: this._name + '/' + path,
        Key: toDir !== '' ? toDir + '/' + newFileName : newFileName
      })
    );

    // in the case of renaming a directory, move files to new location
    if (isDir) {
      // get list of content from old directory
      const command = new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: path
      });

      let isTruncated: boolean | undefined = true;

      while (isTruncated) {
        const { Contents, IsTruncated, NextContinuationToken } =
          await this._s3Client.send(command);

        if (Contents) {
          Contents.forEach(c => {
            const fileName = c.Key!.split('/')[c.Key!.split.length - 1];
            this.copy_file(fileName, path, newFileName, this._name);
          });
        }
        if (isTruncated) {
          isTruncated = IsTruncated;
        }
        command.input.ContinuationToken = NextContinuationToken;
      }
    }

    // retrieve information of new file
    const newFileContents = await this._s3Client.send(
      new GetObjectCommand({
        Bucket: this._name,
        Key: toDir !== '' ? toDir + '/' + newFileName : newFileName
      })
    );
    const [fileType, fileMimeType, fileFormat] = this.getFileType(
      newFileName.split('.')[1]
    );

    data = {
      name: newFileName,
      path: toDir + '/' + newFileName,
      last_modified: newFileContents.LastModified!.toISOString(),
      created: new Date().toISOString(),
      content: await newFileContents.Body!.transformToString(),
      format: fileFormat as Contents.FileFormat,
      mimetype: fileMimeType,
      size: newFileContents.ContentLength!,
      writable: true,
      type: fileType
    };

    // manually refresh filebrowser contents
    this._fileBrowserModel!.refresh();

    this._fileChanged.emit({
      type: 'new',
      oldValue: null,
      newValue: data
    });
    Contents.validateContentsModel(data);
    return data;
  }

  /**
   * Copy a file into another bucket.
   *
   * @param path - The original file path.
   *
   * @param toDir - The destination directory path.
   *
   * @param bucketName - The name of the bucket where content is moved.
   *
   * @returns A promise which resolves with the new contents model when the
   *  file is copied.
   */
  async copyToAnotherBucket(
    path: string,
    toDir: string,
    bucketName: string,
    options: Contents.ICreateOptions = {}
  ): Promise<Contents.IModel> {
    path =
      path[path.length - 1] === '/' ? path.substring(0, path.length - 1) : path;

    // check if we are dealing with a directory
    const info = await this.s3Client.send(
      new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: path
      })
    );

    let isDir: boolean = false;
    if (
      info.Contents!.length > 1 ||
      info.Contents![0].Key![info.Contents![0].Key!.length - 1] === '/'
    ) {
      isDir = true;
    }

    const newFileName = await this.incrementCopyName(path, isDir, bucketName);
    path = isDir ? path + '/' : path;

    // copy file to another bucket
    await this._s3Client.send(
      new CopyObjectCommand({
        Bucket: bucketName,
        CopySource: this._name + '/' + path,
        Key: toDir !== '' ? toDir + '/' + newFileName : newFileName
      })
    );

    // in the case of renaming a directory, move files to new location
    if (isDir) {
      // get list of content from old directory
      const command = new ListObjectsV2Command({
        Bucket: this._name,
        Prefix: path
      });

      let isTruncated: boolean | undefined = true;

      while (isTruncated) {
        const { Contents, IsTruncated, NextContinuationToken } =
          await this._s3Client.send(command);

        if (Contents) {
          Contents.forEach(c => {
            const fileName = c.Key!.split('/')[c.Key!.split.length - 1];
            this.copy_file(fileName, path, newFileName, bucketName);
          });
        }
        if (isTruncated) {
          isTruncated = IsTruncated;
        }
        command.input.ContinuationToken = NextContinuationToken;
      }
    }

    // retrieve information of new file
    const newFileContents = await this._s3Client.send(
      new GetObjectCommand({
        Bucket: bucketName,
        Key: toDir !== '' ? toDir + '/' + newFileName : newFileName
      })
    );
    const [fileType, fileMimeType, fileFormat] = this.getFileType(
      newFileName.split('.')[1]
    );

    data = {
      name: newFileName,
      path: toDir + '/' + newFileName,
      last_modified: newFileContents.LastModified!.toISOString(),
      created: new Date().toISOString(),
      content: await newFileContents.Body!.transformToString(),
      format: fileFormat as Contents.FileFormat,
      mimetype: fileMimeType,
      size: newFileContents.ContentLength!,
      writable: true,
      type: fileType
    };

    this._fileChanged.emit({
      type: 'new',
      oldValue: null,
      newValue: data
    });
    Contents.validateContentsModel(data);
    return data;
  }

  /**
   * Create a checkpoint for a file.
   *
   * @param path - The path of the file.
   *
   * @returns A promise which resolves with the new checkpoint model when the
   *   checkpoint is created.
   */
  async createCheckpoint(path: string): Promise<Contents.ICheckpointModel> {
    const emptyCheckpoint: Contents.ICheckpointModel = {
      id: '',
      last_modified: ''
    };
    return Promise.resolve(emptyCheckpoint);
  }

  /**
   * List available checkpoints for a file.
   *
   * @param path - The path of the file.
   *
   * @returns A promise which resolves with a list of checkpoint models for
   *    the file.
   */
  listCheckpoints(path: string): Promise<Contents.ICheckpointModel[]> {
    return Promise.resolve([]);
  }

  /**
   * Restore a file to a known checkpoint state.
   *
   * @param path - The path of the file.
   *
   * @param checkpointID - The id of the checkpoint to restore.
   *
   * @returns A promise which resolves when the checkpoint is restored.
   */
  restoreCheckpoint(path: string, checkpointID: string): Promise<void> {
    return Promise.reject('Repository is read only');
  }

  /**
   * Delete a checkpoint for a file.
   *
   * @param path - The path of the file.
   *
   * @param checkpointID - The id of the checkpoint to delete.
   *
   * @returns A promise which resolves when the checkpoint is deleted.
   */
  deleteCheckpoint(path: string, checkpointID: string): Promise<void> {
    return Promise.reject('Read only');
  }

  /**
   * Helping function for extracting region of bucket.
   * @returns region of Bucket
   */
  private async getRegion() {
    const response = await this._s3Client.send(
      new GetBucketLocationCommand({
        Bucket: this._name
      })
    );
    return (response?.LocationConstraint as string) ?? '';
  }
  /**
   * Helping function for copying the files inside a directory
   * to a new location, in the case of renaming or copying a directory.
   *
   * @param fileName name of file to be copied
   * @param oldPath old path of file
   * @param newPath new path of file
   */
  private async copy_file(
    fileName: string,
    oldPath: string,
    newPath: string,
    bucketName: string
  ) {
    await this._s3Client.send(
      new CopyObjectCommand({
        Bucket: bucketName,
        CopySource: this._name + '/' + oldPath + fileName,
        Key: newPath + fileName
      })
    );
  }

  /**
   * Helping function for deleting files inside
   * a directory, in the case of deleting the directory.
   *
   * @param filePath complete path of file to delete
   */
  private async delete_file(filePath: string) {
    await this.s3Client.send(
      new DeleteObjectCommand({
        Bucket: this._name,
        Key: filePath
      })
    );
  }

  /**
   * Get all registered file types and store them accordingly with their file
   * extension (e.g.: .txt, .pdf, .jpeg), file mimetype (e.g.: text/plain, application/pdf)
   * and file format (e.g.: base64, text).
   *
   * @param app
   */
  getRegisteredFileTypes(app: JupyterFrontEnd) {
    // get called when instating the toolbar
    const registeredFileTypes = app.docRegistry.fileTypes();

    for (const fileType of registeredFileTypes) {
      // check if we are dealing with a directory
      if (fileType.extensions.length === 0) {
        this._registeredFileTypes[''] = {
          fileType: 'directory',
          fileFormat: 'json',
          fileMimeTypes: ['text/directory']
        };
      }

      // store the mimetype and fileformat for each file extension
      fileType.extensions.forEach(extension => {
        extension = extension.split('.')[1];
        if (!this._registeredFileTypes[extension]) {
          this._registeredFileTypes[extension] = {
            fileType: fileType.name,
            fileMimeTypes: [...fileType.mimeTypes],
            fileFormat: fileType.fileFormat ? fileType.fileFormat : ''
          };
        }
      });
    }
  }

  /**
   * Helping function to define file type, mimetype and format based on file extension.
   * @param extension file extension (e.g.: txt, ipynb, csv)
   * @returns
   */
  private getFileType(extension: string) {
    let fileType: string = 'text';
    let fileMimetype: string = 'text/plain';
    let fileFormat: string = 'text';
    extension = extension ?? '';

    if (this._registeredFileTypes[extension]) {
      fileType = this._registeredFileTypes[extension].fileType;
      fileMimetype = this._registeredFileTypes[extension].fileMimeTypes[0];
      fileFormat = this._registeredFileTypes[extension].fileFormat;
    }

    // the file format for notebooks appears as json, but should be text
    if (extension === 'ipynb') {
      fileFormat = 'text';
    }

    return [fileType, fileMimetype, fileFormat];
  }

  private _serverSettings: ServerConnection.ISettings;
  private _s3Client: S3Client;
  private _name: string = '';
  private _provider: string = '';
  private _baseUrl: string = '';
  private _region: string = '';
  private _creationDate: string = '';
  private _fileChanged = new Signal<this, Contents.IChangedArgs>(this);
  private _isDisposed: boolean = false;
  private _disposed = new Signal<this, void>(this);
  private _registeredFileTypes: IRegisteredFileTypes = {};
  private _fileBrowserModel: FileBrowserModel | undefined;
}

export namespace Drive {
  /**
   * The options used to initialize a `Drive`.
   */
  export interface IOptions {
    /**
     * S3 client configuration if available
     */
    config?: S3ClientConfig;

    /**
     * The name for the `Drive`, which is used in file
     * paths to disambiguate it from other drives.
     */
    name: string;

    /**
     * The server settings for the server.
     */
    serverSettings?: ServerConnection.ISettings;
  }
}
