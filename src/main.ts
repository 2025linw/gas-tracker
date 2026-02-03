import { createApp } from 'vue';
import { VueFire, VueFireAuth } from 'vuefire';
import { createPinia } from 'pinia';

import { app as firebaseApp } from './firebase';
import router from './router';

import App from './App.vue';

const app = createApp(App);

app.use(router);
app.use(createPinia());

app.use(VueFire, {
  firebaseApp,
  modules: [VueFireAuth()],
});


app.mount('#app');
