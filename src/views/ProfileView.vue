<script setup lang="ts">
import { collection, doc, updateDoc } from 'firebase/firestore';
import { computed } from 'vue';
import { useCollection, useCurrentUser, useDocument, useFirebaseAuth, useFirestore } from 'vuefire';

import type { TThemeOptions, TUser } from '@/types';

import { signOut } from 'firebase/auth';
import { useRouter } from 'vue-router';
import { useThemePreferences } from '@/composables/useThemePreferences';

const router = useRouter();

const auth = useFirebaseAuth()!;
const db = useFirestore();
const user = useCurrentUser();

const { setTheme } = useThemePreferences();

const userRef = computed(() => (user.value ? doc(db, 'users', user.value.uid) : null));
const userPrefs = useDocument<TUser>(userRef);

const vehiclesRef = computed(() =>
  user.value ? collection(db, 'users', user.value.uid, 'vehicles') : null,
);
const vehicles = useCollection(vehiclesRef);

async function setUserTheme(value: TThemeOptions) {
  if (!user.value) return null;

    const userDocRef = doc(db, 'users', user.value.uid);

    await updateDoc(userDocRef, {
      themePref: value,
    });

    return value;
}

async function logout() {
  await signOut(auth);

  router.push('splash');
}
</script>

<template>
  <h1 v-if="!user" class="title is-1">Hey {{ user?.displayName }}!</h1>

  <h2 class="title is-3">Theme</h2>

  <div class="buttons has-addons">
    <button class="button" :class="{ 'is-primary is-selected': userPrefs?.themePref === 'system' }"
      @click="setUserTheme('system'); setTheme('system');">
      System
    </button>
    <button class="button" :class="{ 'is-light is-selected': userPrefs?.themePref === 'light' }"
      @click="setUserTheme('light'); setTheme('light');">
      Light
    </button>
    <button class="button" :class="{ 'is-dark is-selected': userPrefs?.themePref === 'dark' }"
      @click="setUserTheme('dark'); setTheme('dark');">
      Dark
    </button>
  </div>

  <div id="footer">
    <div class="buttons is-centered">
      <button class="button is-warning" @click="logout">Logout</button>
    </div>
  </div>
</template>

<style scoped>
  #footer {
    width: 100%;

    position: fixed;
    bottom: 0;

    padding-bottom: 5rem;
  }
</style>
