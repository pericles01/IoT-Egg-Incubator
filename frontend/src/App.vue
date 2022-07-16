<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        
        target="_blank"
        text
      >
        <span class="mr-2">Egg Incubator Remote App</span>
        
      </v-btn>
    </v-app-bar>

    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app> 
</template>

<script>

import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',
  components: {
    HelloWorld
  },

}
</script>

