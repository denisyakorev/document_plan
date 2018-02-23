function initial(){
            //Загрузка CKEditor
           var inline_editing = document.getElementsByClassName('inline_editing');
           var id;
           for (elem in inline_editing){
                id = inline_editing[elem].id;
                load_editor(id);
           }
            console.log("Hello world");
           //Реализация добавления строк
           $('#add_row_btn').click(function(){
               console.log("Hello world");
               add_new_row('chapters_table');
           })

}

function load_editor(name){
    var editor = CKEDITOR.instances[name];
    if (editor) { editor.destroy(true); }
    CKEDITOR.inline( name, {
                toolbarGroups: [
                    {"name":"basicstyles","groups":["basicstyles"]},
                    {"name":"paragraph","groups":["list","indentlist"]},
                    {"name":"document","groups":["mode"]},

                ],

                extraPlugins: 'sourcedialog,bbcode',
                removeButtons: 'Underline,Strike,Subscript,Superscript,NewPage',
                startupFocus: false
                });
           }


/*Используется глобальная переменные button_up_name и num_of_rows - из шаблона django*/
function add_new_row(table_id){
    //Получаем шаблон из файла templates.js по id
    var source   = document.getElementById("new_chapter_row").innerHTML;
    var template = Handlebars.compile(source);
    var context = {button_up_name: button_up_name, num_of_rows: num_of_rows};
    var html    = template(context);
    var table = $('#' + table_id + ' > tbody:last-child').append(new_row);
    num_of_rows += 1;

}

$(document).ready(function(){
    initial();
});