<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useCurrentUser } from 'vuefire';

import icon from '../assets/img/gas_can.png';

import { useAuth } from '@/composables/useAuth';

const router = useRouter();

const user = useCurrentUser();
const { loginWithGoogle } = useAuth();

onMounted(() => {
  // Toggle Menu on Mobile
  const navBurger = document.getElementById('nav-burger')!;
  const navMenu = document.getElementById('nav-menu')!;
  navBurger.addEventListener('click', () => {
    navBurger.classList.toggle('is-active');
    navMenu.classList.toggle('is-active');
  });
});
</script>

<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <RouterLink class="navbar-item" to="/">
        <img :src="icon" />
      </RouterLink>

      <button id="nav-burger" class="navbar-burger">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <div id="nav-menu" class="navbar-menu">
      <div class="navbar-start">
        <RouterLink class="navbar-item" to="/">Dashboard</RouterLink>
        <RouterLink class="navbar-item" to="/trends">Trends</RouterLink>
        <RouterLink class="navbar-item" to="/records">Records</RouterLink>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <button v-if="user" class="button">Add Gas Data</button>

            <button v-if="user" class="button is-primary" @click="router.push('/profile')">
              View Profile
            </button>
            <div v-else class="buttons">
              <button class="button is-primary" @click="loginWithGoogle">Login</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
