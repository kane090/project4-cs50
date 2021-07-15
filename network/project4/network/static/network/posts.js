function edit_post(post_id) {

    // Finding and removing content
    let post_div = document.querySelector(`#post_div_${post_id}`);
    let area_to_replace = post_div.children[0];
    const content = area_to_replace.innerHTML;
    area_to_replace.remove();

    // Replacing content with textarea and inserting it
    let text_area = document.createElement('textarea');
    text_area.id = 'edit_textarea';
    text_area.innerHTML = content;
    text_area.rows = 4;
    text_area.cols = 45;
    text_area.setAttribute('required', 'true');
    post_div.insertBefore(text_area, post_div.firstChild);
    let line_break = document.createElement('br');
    text_area.parentNode.insertBefore(line_break, text_area.nextSibling);

    let button = document.querySelector(`#edit_${post_id}`);
    button.setAttribute('type', 'button');
    button.id = `save_${post_id}`;
    button.onclick = function() {
        save_post(post_id);
    }
    button.innerHTML = 'Save';
}


function save_post(post_id) {

    // Getting new content from textarea
    const new_content = document.querySelector('#edit_textarea').value;

    // Saving content
    fetch(`/edit/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: new_content
        })
    })

    // Restoring previous view with new content
    let post_div = document.querySelector(`#post_div_${post_id}`);
    let area_to_replace = post_div.children[0];
    area_to_replace.remove();

    let paragraph = document.createElement('p');
    paragraph.innerHTML = new_content;
    post_div.insertBefore(paragraph, post_div.firstChild);
    post_div.removeChild(paragraph.nextSibling);

    let button = document.querySelector(`#save_${post_id}`);
    button.setAttribute('type', 'button');
    button.id = `edit_${post_id}`;
    button.onclick = function() {
        edit_post(post_id);
    }
    button.innerHTML = 'Edit';
}


// function like_post(post_id) {
    
//     fetch(`/like/${post_id}`, {
//         method: 'PUT',
//         body: JSON.stringify({
//         })
//     })
// }
