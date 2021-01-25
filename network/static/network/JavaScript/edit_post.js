document.addEventListener("DOMContentLoaded", () => {

    // Gets all the editable posts' buttons from the list
    const edit_btn = document.querySelectorAll(".edit");
    
    // For each edit button adds a click event listener
    edit_btn.forEach(element => {
        element.addEventListener("click", event =>{

            // Gets the button that was clicked and disables it while editing content
            const edit_btn = event.target;
            edit_btn.disabled = true;

            // Gets the targeted post id, it's content and content container (div)
            const post_id = element.dataset.post_id;
            const post_content_container = document.querySelector(`#post-${post_id}`);
            const post_content = document.querySelector(`#post-${post_id} > span`);

            // Hide the current content
            document.querySelector(`#hide-${post_id}`).style.display = "none";
            
            // Creates an editing span element to include textare and Save and Cancel button
            const edit_content = document.createElement("span");

            // Populates the editing span element
            edit_content.innerHTML = `
                <textarea id="content-${post_id}" name="content">${post_content.innerHTML}</textarea>
                <div>
                    <button id="save-${post_id}" class="btn btn-sm btn-outline-success">Save</button>
                    <button id="cancel-${post_id}" class="btn btn-sm btn-outline-danger">Cancel</button>
                </div>`;

            // Shows the editing span element by appending it in the content container
            post_content_container.appendChild(edit_content);

            // Clicking on save
            document.querySelector(`#save-${post_id}`).addEventListener("click", () => {

                // Gets the edited content (from the textarea)
                const new_content = document.querySelector(`#content-${post_id}`).value;

                // Checks for empty or same content. If so, shows alerts.
                if (new_content === "") {
                    alert("The content can not be empty !");
                } else if (new_content === post_content.innerHTML){
                    alert(`The new content must be different !`)
                } else {

                    // Makes ajax call to save new content
                    edit_post(post_id, new_content).then(updated_content => {

                        // Enables edit button
                        edit_btn.disabled = false;

                        // Removes the editing span element
                        post_content_container.removeChild(edit_content);

                        // Populates the former content with the updated content and displays it
                        post_content.innerHTML = updated_content;
                        document.querySelector(`#hide-${post_id}`).style.display = "block";
                    });
                }
            });

            // Clicking on cancel
            document.querySelector(`#cancel-${post_id}`).addEventListener("click", () => {

                // Enables edit button
                edit_btn.disabled = false;

                // Removes the editing span element
                post_content_container.removeChild(edit_content);
                
                // Shows the uneditted content
                document.querySelector(`#hide-${post_id}`).style.display = "block";
            });
        });
    });
});