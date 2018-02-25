

$(document).ready(function(){
    get_data();
    init_table();
});


//Получение данных для построения таблицы от сервера
function get_data(){
    var result;
    var plan_id = $('#plan_name').attr('js-plan-id');
    if (!plan_id){ plan_id = 'new' };
     $.ajax({
        type: 'GET',
        url: '/docplan/'+plan_id+'/ajax/chapters/',
        success: function (data, textStatus) {
            create_table(data);
        },
        error: function(xhr, status, e) {
            alert(status, e);
        }
    });
}


function init_table(){
    $("#delete-row-btn").bind('click', deleteRows);
}


function deleteRows(){
    $('[id ^= chapter_checkbox_]').each(function(){
        if($(this).prop('checked')){
            $(this).closest('tr').detach();
        }
    });
}


function init_row(rowId){
    $('#chapter_checkbox_'+rowId).bind('change', toggleDeleteBtn);
}


function toggleDeleteBtn(){
    var checked = false;
    $('[id ^= chapter_checkbox_]').each(function(){
        if($(this).prop('checked')){
            $("#delete-row-btn").show();
            checked = true;
        }
    });

    if (!checked){
        $("#delete-row-btn").hide();
    }

}


function create_table(data){
    var template = $("#new_chapter_row").html();
    var container = $("#chapters-container");
    var context;

    if (data.content.chapters.length == 0){
        chapters = [{
            'id': 'new_0',
            'name': ' ',
            'questions': ' '
        }];
    }else{
        chapters = data.content.chapters;
    }

    $(container).empty();
    for (chapter in chapters){
        context = {
            'chapter': chapters[chapter]
        }
        if(chapter == 0){
            context['showUpBtn'] = false;
        }else{
            context['showUpBtn'] = true;
        }

        $(container).append(Mustache.render(template, context));
        init_row(context.chapter.id);

    }
}




