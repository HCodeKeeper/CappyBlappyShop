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