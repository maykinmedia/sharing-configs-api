import { JSONEditor } from '@json-editor/json-editor';

import { jsonScriptToVar} from '../utils/json-script';


class Editor {

    constructor(node) {
        this.node = node;
        this.schemas = jsonScriptToVar('jsonSchemas');

        this.inputNode = document.getElementById(node.dataset.inputFieldId);
        this.typeNode = document.getElementById(node.dataset.typeFieldId);
        this.typeNode.addEventListener('change', this.changeType.bind(this));

        this.jsonEditor = this.displayJsonEditor(this.typeNode.value);
    }

    displayJsonEditor(schema_type) {
        const schema = this.schemas[schema_type] || {};
        schema.title = 'JSON editor';
        const jsonEditor = new JSONEditor(
            this.node,
            {'schema': schema, 'no_additional_properties': true}
        );

        if (this.inputNode.value) {
            const json = JSON.parse(this.inputNode.value);
            jsonEditor.setValue(json);
        }

        jsonEditor.on('change', () => {
            const errors = jsonEditor.validate();
            if (errors.length) {
                console.log(errors);
            }
            else {
                const json = jsonEditor.getValue();
                this.inputNode.value = JSON.stringify(json);
            }
        });

        return jsonEditor;
    }

    changeType(event) {
        this.jsonEditor.destroy();
        this.jsonEditor = this.displayJsonEditor(event.target.value);
    };

}


const editor_node = document.getElementById('json-editor');

if (editor_node) {
    new Editor(editor_node);
}
