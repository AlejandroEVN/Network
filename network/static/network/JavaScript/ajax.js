// call to follow/unfollow an user
async function toggle_follow(user_id) {
    const response = await fetch(`${user_id}/follow`, {
        method: "PUT"
    });

    const updated_follow = await response.json();

    return updated_follow;
}

// call to update the content of the editable post
async function edit_post(post_id, content) {
    const response = await fetch(`edit/${post_id}`, {
        method: "PUT",
        body: JSON.stringify ({
            content: content
        })
    });
    const updated_content = await response.json();

    return updated_content;
}

// call to toggle like/unlike status in post
async function like_post(post_id, liked) {
    const response = await fetch(`like/${post_id}`, {
        method: "PUT",
        body: JSON.stringify ({
            liked: liked
        })
    });
    const updated_likes = await response.json();

    return updated_likes;
}