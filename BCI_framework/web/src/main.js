import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import Vuelidate from 'vuelidate';
import 'bootstrap/dist/css/bootstrap.min.css'

import Video from 'video.js'
import 'video.js/dist/video-js.css'

Vue.use(Vuelidate);
Vue.prototype.$video = Video

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: function(h) {
    //return h(App);
    return h(App);
  },
}).$mount("#app");
