// Time zone effect handlers
let tz_select = document.getElementById("select-timezone");
let user_timezone_opt = document.getElementById("user-timezone");
let get_user_timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

user_timezone_opt.value = get_user_timezone;
user_timezone_opt.innerHTML = get_user_timezone;

tz_select.addEventListener("change", function(){
    url_addr = window.location.origin + window.location.pathname + `?tz=${this.value}`;
    window.location.replace(`${url_addr}`);
})
// Time zone effect handlers

// Upward scroll effect handlers
const btn_upward = document.getElementById("up_button");
const rootElement = document.documentElement;

btn_upward.addEventListener("click", function(){
    rootElement.scrollTo({
    top: 300,
    behavior: "smooth"
  })
})

function handleScroll() {
  // Do something on scroll
  let scrollTotal = rootElement.scrollHeight - rootElement.clientHeight
  if ((rootElement.scrollTop / scrollTotal ) > 0.15 ) {
    // Show button
    btn_upward.classList.add("block");
    btn_upward.classList.remove("hidden")
  } else {
    // Hide button
    btn_upward.classList.remove("block");
    btn_upward.classList.add("hidden")
  }
}

document.addEventListener("scroll", handleScroll)
// Upward scroll effect handlers