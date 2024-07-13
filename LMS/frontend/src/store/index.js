import { createStore } from 'vuex';

export default createStore({
  state: {
    alertMessage: null,
  },
  mutations: {
    setAlert(state, alertMessage) {
      state.alertMessage = alertMessage;
    },
    clearAlert(state) {
      state.alertMessage = null;
    },
  },
  actions: {
    updateAlert({ commit }, alertMessage) {
      commit('setAlert', alertMessage);
    },
  },
  getters: {
    alertMessage: (state) => state.alertMessage,
  }
});
