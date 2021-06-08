import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    withBackend: true,
    // backend_url: "http://0.0.0.0:8081",  /** Deploy the server locally, website avaliable only on itself */
    backend_url: "http://10.245.71.200:8081", /** Deploy the server to a specific IP address, website available on local network */
    sessionIndex: -1,
    currentSession: null,
    numberOfSessions: 0,
    serialIndex: -1,
    currentSerial: null,
  },
  mutations: {},
  actions: {},
  modules: {}
});
