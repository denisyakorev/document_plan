<script id="new_chapter_row" type="text/x-handlebars-template">
    <tr>
        <td>
          <div class="d-flex justify-content-center align-items-center">
            <input type="checkbox" class="chapter_checkbox">
          </div>
        </td>
        <td><div id="chapter_name_{{row_counter}}" class="inline_editing" contenteditable="true">{{chapter.name}}</div></td>
        <td><div id="chapter_questions_{{row_counter}}" class="inline_editing" contenteditable="true">{{chapter.questions|safe}}</div></td>
        <td>
          <div class="d-flex justify-content-center align-items-center">
            <a class="btn" href="">{{button_up_name}}</a>
          </div>
        </td>
    </tr>
  </script>
