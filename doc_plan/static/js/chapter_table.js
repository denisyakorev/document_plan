var CONTAINER_ID = 'chapters-container';
var ROW_TEMPLATE_ID = 'new_chapter_row';
var PLAN_ID_HOLDER = 'plan_name';
var PLAN_ID_ATTR = 'js-plan-id';

var DELETE_ROW_BTN_ID = 'delete-row-btn';
var ADD_ROW_BTN_ID = 'add-row-btn';
var CHECKBOX_PREFIX = 'chapter_checkbox_';
var CHAPTER_NAME_PREFIX = 'chapter_name_';
var CHAPTER_QUESTION_PREFIX = 'chapter_questions_';
var UP_BTN_PREFIX = 'upBtn_';
var COUNTER = 0;




/*--------------------------------------
-----------LIBS CONFIG-------------------
-------------------------------------*/


var toolbarsGroup_basic = [
                {"name": "basicstyles", "groups": ["basicstyles"]},
                {"name": 'clipboard', "groups": [ 'selection', 'clipboard' ] },
                {"name": "document", "groups": ["mode"]},
            ];

var toolbarsGroup_extend = [
                {"name": "basicstyles", "groups": ["basicstyles"]},
                {"name":"paragraph","groups":["list","indentlist"]},
                {"name": 'clipboard', "groups": [ 'selection', 'clipboard' ] },
                {"name": "document", "groups": ["mode"]},
            ];
var extraPlugins = 'sourcedialog,bbcode';
var removeButtons = 'Underline,Strike,Subscript,Superscript,NewPage';
var startupFocus = false;

//CKEditor
CKEDITOR.on( 'instanceCreated', function ( event ) {
    var editor = event.editor,
            element = editor.element;

    editor.on( 'configLoaded', function () {

        // Customize editors for headers and tag list.
        if ( element.is( 'h1', 'h2', 'h3' )) {

            editor.config.toolbarGroups= toolbarsGroup_basic;

        }else{
            editor.config.toolbarGroups= toolbarsGroup_extend;
        }

        editor.config.extraPlugins= extraPlugins;
        editor.config.removeButtons= removeButtons;
        editor.config.startupFocus= startupFocus;
    });
} );




//Mustache
Mustache.tags = ['[[', ']]'];




/*--------------------------------------------------
-----------------SCRIPT BODY------------------------
--------------------------------------------------*/


$(document).ready(function(){
    getData();
    initTable();
});


//Получение данных для построения таблицы от сервера
function getData(){
    var result;

    var plan_id = $('#' + PLAN_ID_HOLDER).attr(PLAN_ID_ATTR);
    if (!plan_id){ plan_id = 'new' };
    var URL = '/docplan/'+plan_id+'/ajax/chapters/';

     $.ajax({
        type: 'GET',
        url: URL,
        success: function (data, textStatus) {
            createTable(data);
        },
        error: function(xhr, status, e) {
            alert(status, e);
        }
    });
}


//Создание таблицы по полученным данным
function createTable(data){

    var context;
    var container = $("#" + CONTAINER_ID);

    if (data.content.chapters.length == 0){
        chapters = [{
            'id': 'new_0',
            'name': ' ',
            'questions': ' '
        }];
        COUNTER += 1;
    }else{
        chapters = data.content.chapters;
    }

    $(container).empty();
    for (chapter in chapters){
        context = {
            'chapter': chapters[chapter]
        }
       createRow(context);

    }

    toggleUpBtn();
}


function createRow(context){

    var container = $("#" + CONTAINER_ID);
    var template = $("#" + ROW_TEMPLATE_ID).html();
    $(container).append(Mustache.render(template, context));
    initRow(context.chapter.id);
}


//Инициализация событий на общих для всей таблицы элементах
function initTable(){
    $("#" + DELETE_ROW_BTN_ID).bind('click', deleteRows);
    $("#" + ADD_ROW_BTN_ID).bind('click', addRow);
}


//Инициализация событий на отдельной строке
function initRow(rowId){
    $('#' + CHECKBOX_PREFIX + rowId).bind('change', toggleDeleteBtn);
    $('#' + UP_BTN_PREFIX + rowId).bind('click', moveUp);

    $('#' + CHAPTER_NAME_PREFIX + rowId).add('#' + CHAPTER_QUESTION_PREFIX + rowId).each(function(){
        CKEDITOR.inline($(this).attr('id'), {
			toolbarGroups: toolbarsGroup_extend,
			extraPlugins: extraPlugins,
			removeButtons: removeButtons,
			startupFocus: startupFocus

            });
    });

}


function deleteRows(){
    $('[id ^= ' + CHECKBOX_PREFIX + ']').each(function(){
        if($(this).prop('checked')){
            $(this).closest('tr').detach();
        }
    });

    toggleDeleteBtn();
}


function addRow(){
    var context = {
        'chapter': {
            'id': 'new_' + COUNTER,
            'name': ' ',
            'questions': ' '
        }
    }

    createRow(context);
    COUNTER += 1;
}


function moveUp(event){
    tr = $(event.target).closest('tr');
    tr.after(tr.prev());
    toggleUpBtn();
}



function toggleUpBtn(){
    $('#' + CONTAINER_ID + " tr:first button").hide();
    $('#' + CONTAINER_ID + " tr:eq(1) button").show();
}



function toggleDeleteBtn(){
    var checked = false;
    $('[id ^= ' + CHECKBOX_PREFIX + ']').each(function(){
        if($(this).prop('checked')){
            $("#" + DELETE_ROW_BTN_ID).show();
            checked = true;
        }
    });

    if (!checked){
        $("#" + DELETE_ROW_BTN_ID).hide();
    }

}








