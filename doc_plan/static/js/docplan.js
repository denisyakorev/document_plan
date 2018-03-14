var CONTAINER_ID = 'chapters-container';
var ROW_TEMPLATE_ID = 'new_chapter_row';
var PLAN_ID_HOLDER = 'name';
var PLAN_ID_ATTR = 'js-plan-id';
var PLAN_SAVE_BTN_ID = 'save-plan';
var SAVE_FORM_ID = 'save-form';

var DELETE_ROW_BTN_ID = 'delete-row-btn';
var ADD_ROW_BTN_ID = 'add-row-btn';
var CHECKBOX_PREFIX = 'chapter_checkbox_';
var CHAPTER_NAME_PREFIX = 'chapter_name_';
var CHAPTER_QUESTION_PREFIX = 'chapter_questions_';
var UP_BTN_PREFIX = 'upBtn_';
var PLAN_CLASS = 'plan';
var CHAPTERS_CLASS = 'chapters';
var ERROR_MESSAGE_TEMPLATE_ID = 'error_message_template';
var ERROR_MESSAGE_CLASS = 'error_message';
var SUBMIT_ERROR_ID = 'submit_error_template';
var COUNTER = 0;
var URL_GET;
var URL_POST;







/*--------------------------------------
-----------LIBS CONFIG-------------------
-------------------------------------*/


var toolbarsGroup_basic = [
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
    var plan_id = $('#' + PLAN_ID_HOLDER).attr(PLAN_ID_ATTR);
    if (!plan_id){ plan_id = 'new' };
    URL_GET = '/docplan/'+plan_id+'/ajax/chapters/';
    URL_POST = '/docplan/'+plan_id+'/save/';

    getData();
    initPage();

});


//Получение данных для построения таблицы от сервера
function getData(){
    var result;

     $.ajax({
        type: 'GET',
        url: URL_GET,
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

    chapters = data.chapters;

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
    var row_html = Mustache.render(template, context);
    $(container).append(row_html);
    initRow(context.chapter.id);
}


//Инициализация событий на общих для всей страницы элементах
function initPage(){
    $("#" + DELETE_ROW_BTN_ID).bind('click', deleteRows);
    $("#" + ADD_ROW_BTN_ID).bind('click', addRow);
    $("#" + PLAN_SAVE_BTN_ID).bind('click', save);
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

    toggleUpBtn();
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


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function save(){
    //Собираем объект для отправки
    var postData = {};
    var plan = {};

    $('.'+PLAN_CLASS).each(function(){
        plan[$(this).attr("id")] = CKEDITOR.instances[$(this).attr("id")].getData();
    });

    var chapters = [];
    var chapter = {};
    var id;

    $("#" + CONTAINER_ID+" tr").each(function(){
        id = $(this).attr('id');
        name_id = CHAPTER_NAME_PREFIX + id;
        questions_id = CHAPTER_QUESTION_PREFIX + id
        chapter = {
            'id': id,
            'name': CKEDITOR.instances[name_id].getData(),
            'questions': CKEDITOR.instances[questions_id].getData()
        };
        chapters.push(chapter);
    });

    postData['plan'] = JSON.stringify(plan);
    postData['chapters'] = JSON.stringify(chapters);

    var csrftoken = getCookie('csrftoken');

    //Отправляем
    $.ajax({
        url: URL_POST,
        method: "POST",
        data:{
            csrfmiddlewaretoken: csrftoken,
            plan: postData['plan'],
            chapters: postData['chapters']
        },
        success: function (data, textStatus) {
            window.location.replace('/docplan/'+data['plan_id']+'/view/')
        },
        error: function(data, textStatus, e) {
            var response = JSON.parse(data.responseText);
            showErrors(response)


        }

    });
}

function showErrors(response){

    if (response.errors){
        var template = $("#" + ERROR_MESSAGE_TEMPLATE_ID).html();
        var submitErrorTemplate = $("#" + SUBMIT_ERROR_ID).html();
        var context = {};
        $("." + ERROR_MESSAGE_CLASS).detach();
        $("#" + PLAN_SAVE_BTN_ID).before(Mustache.render(submitErrorTemplate, context));

        if(response.errors.plan){
            for (each in response.errors.plan[0]){
                for (elem in response.errors.plan[0][each]){
                    context['error_message'] += response.errors.plan[0][each][elem];
                }
                $("#" + each).before(Mustache.render(template, context));
            }
        }

        var selector = "";
        for (each in response.errors.chapters){
        context['error_message'] = "";
        selector = "#" + response.errors.chapters[each].id
            for (elem in response.errors.chapters[each].errors){
                curError = response.errors.chapters[each].errors[elem]
                cur_selector = selector + " [model-attr = " + elem + "]";
                for (error in curError){
                     context['error_message'] += curError[error];
                }
                $(cur_selector).before(Mustache.render(template, context));

            }

        }

    }
}








