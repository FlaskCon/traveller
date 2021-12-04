function show_indicator(input_tag){
    let remainder_tag = document.querySelector(`.input_${input_tag.name}`);
        // Show indicator
        remainder_tag.classList.add("inline");
        remainder_tag.classList.remove("hidden");

        input_tag.addEventListener('input', function(e){
            let remainder = e.target.maxLength - e.target.value.length;
            remainder_tag.innerHTML = `${remainder}/${e.target.maxLength } max`;
        })
}

function remove_indicator(input_tag){
    let remainder_tag = document.querySelector(`.input_${input_tag.name}`);
        // Remove indicator
        remainder_tag.classList.remove("inline");
        remainder_tag.classList.add("hidden");
}