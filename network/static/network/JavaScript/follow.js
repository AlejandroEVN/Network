document.addEventListener("DOMContentLoaded", () => {

    // Gets the follow/unfollow button
    const follow_btn = document.querySelector("#btn-follow");

    // Followers count
    const followers = document.querySelector("#followers");

    follow_btn.addEventListener("click", () => {
       
        // Gets the targeted profile users' id
        const profile_user_id = follow_btn.dataset.follow;

        // Makes ajax call
        toggle_follow(profile_user_id).then(updated_follow => {
            if (updated_follow.following) {
                follow_btn.innerHTML = "Unfollow";
            } else {
                follow_btn.innerHTML = "Follow";
            }            
            followers.innerHTML = updated_follow.followers;
        });
    });
});