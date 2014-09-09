// String truncation via .trunc()
String.prototype.trunc = String.prototype.trunc ||
  function(n){
    return this.length>n ? this.substr(0,n-1)+'&hellip;' : this;
  };
// Dashboard pane display management
function hide(id) {
  $("#" + id).hide();
}
function hideAll() {
  $('.dash-content').each(function (i, obj) {
    hide(obj.id);
  });
}
function show(id) {
  hide(window["currentPage"]);
  $("#" + id).show();
  window["currentPage"] = id;
  window.history.pushState("", "", "#" + id);
}
// Order status display
function getIcon(status, paid, developer) {
  if (status == '3'){
    if (paid == '0') {
      return "fa-usd";
    } else {
      return "fa-check-circle";
    }
  } else {
    if (paid == '1') {
      return "fa-spinner fa-spin";
    } else if (!developer){
      return "fa-times-circle";
    } else {
      return "fa-question";
    }
  }
}
function getStatus(status) {
  if (status == 0){
    return "Created";
  } else if (status == 1){
    return "Start";
  } else if (status == 2){
    return "Ïn Progress";
  } else if (status == 3){
    return "Done";
  }
  return "Undefined";
}
// Plugin / Order template handlers
function insertTablePlugin(plugin) {
  var rendered_template = $('#plugin-table-template').tmpl(plugin);
  $('#plugin-table').append(rendered_template);
  pluginDetailOnClick(plugin);
}
function pluginDetailOnClick(plugin) {
  var rendered_template = $('#plugin-detail-template').tmpl(plugin);
  $("#order-" + plugin.order_id).on("click", function(e) {
    e.preventDefault();
    $('#plugin-detail').empty();
    $('#plugin-detail').append(rendered_template);
  })
}
// Application API calls
function getUserOrders(user_id) {
  return $.ajax({
    url: "/api/users/" + user_id + "/orders/",
    context: document.body
  });
}
function getUser(user_id) {
  return $.ajax({
    url: "/api/users/" + user_id,
    context: document.body
  });
}
function getOrder(order_id) {
  return $.ajax({
    url: "/api/orders/" + order_id,
    context: document.body
  });
}
function getPlugin(plugin_id) {
  return $.ajax({
    url: "/api/plugins/" + plugin_id,
    context: document.body
  });
}