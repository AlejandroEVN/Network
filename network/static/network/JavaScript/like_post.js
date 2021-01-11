document.addEventListener("DOMContentLoaded", () => {

    // Gets all the like buttons (not own posts like buttons)
    const like_btn = document.querySelectorAll(".like");

    // Adds click event to each button
    like_btn.forEach(button => {
        button.addEventListener("click", event => {

            // Gets the clicked button
            const target_btn = event.target;

            // Gets the targeted post id
            const post_id = target_btn.dataset.post_id;

            // Stores whether the post is liked by the requesting user
            const liked = target_btn.dataset.liked === "true";
            
            // Gets the span element containing the number of likes for that post
            const post_likes = document.querySelectorAll(`#likes-${post_id}`)[0];

            // Ajax call to add or remove like
            like_post(post_id, liked).then(updated_likes => {

                // If the post is liked after toggling
                if (updated_likes.liked) {
                    target_btn.dataset.liked = "true";
                    target_btn.innerHTML = "favorite";
                // else the post is not liked after toggling
                } else {
                    target_btn.dataset.liked = "false";
                    target_btn.innerHTML = "favorite_border";
                }                

                // Updates number of likes in the HTML
                post_likes.innerHTML = updated_likes.post_likes;
            });
        });
    });
});