//CKEditor
CKEDITOR.on( 'instanceCreated', function ( event ) {
    var editor = event.editor,
            element = editor.element;

    editor.on( 'configLoaded', function () {

        // Customize editors for headers and tag list.
        if ( element.is( 'h1', 'h2', 'h3' )) {

            editor.config.toolbarGroups= [
                {"name": "basicstyles", "groups": ["basicstyles"]},
                {"name": 'clipboard', "groups": [ 'selection', 'clipboard' ] },
                {"name": "document", "groups": ["mode"]},
            ];

        }else{
            editor.config.toolbarGroups= [
                {"name": "basicstyles", "groups": ["basicstyles"]},
                {"name":"paragraph","groups":["list","indentlist"]},
                {"name": 'clipboard', "groups": [ 'selection', 'clipboard' ] },
                {"name": "document", "groups": ["mode"]},
            ];
        }

        editor.config.extraPlugins= 'sourcedialog,bbcode';
        editor.config.removeButtons= 'Underline,Strike,Subscript,Superscript,NewPage';
        editor.config.startupFocus= false;
    });
} );




//Mustache
Mustache.tags = ['[[', ']]'];