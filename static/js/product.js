api_path_to_add = "/cart/item/add/";


const MIN = 1;
const MAX = 100;

function getCSRF() {
    let name = "csrftoken";
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function get_element(){
    return document.getElementsByClassName("body_section")[0];
}


function clear_element(element){
    element.innerHTML = "";
}


function render_description(text){
    let section = get_element();
    clear_element(section);
    let text_element = document.createElement("p");
    text_element.appendChild(document.createTextNode(text));
    section.appendChild(text_element);
}


function render_contacts(manufacturer, contact_info){
    let section = get_element();
    clear_element(section);
    let manufacturer_element = document.createElement("p");
    manufacturer_element.setAttribute("id", "manufacturer");
    manufacturer_element.appendChild(document.createTextNode(manufacturer));
    section.appendChild(manufacturer_element)

    let contacts_info = document.createElement("p");
    contacts_info.setAttribute("id", "contacts");
    contacts_info.appendChild(document.createTextNode(contact_info));
    section.appendChild(contacts_info);
}

function boundaries(number, min, max){
    return (number >= min && number <= max);
}

function validate_number(number, min, max){
    let is_valid = false;
    if (!isNaN(number)){
        is_valid = boundaries(number, min, max);
    }
    return is_valid;
}


function add_to_cart(product_id){
    let count = document.getElementById("counter").value;
    let addon_id = document.getElementById("addons").value;
    if (!validate_number(count, MIN, MAX)){
        return;
    }

    let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {

    }
  }
  xhttp.open("POST", api_path_to_add, true);

  xhttp.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhttp.setRequestHeader("X-CSRFToken", getCSRF());
  xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  if (!isNaN(parseInt(count)) && parseInt(count) >= 1){
      xhttp.send(JSON.stringify(
          {payload:{
          "product_id" : product_id,
          "count" : count,
          "addon_id" : addon_id
      }}
  ));
  }
}