<script setup lang="ts">
import { watch } from 'vue';
import { useCurrentUser, useDocument, useFirestore } from 'vuefire';
import { doc } from 'firebase/firestore';

import type { TUser } from '@/types';
import NavBar from '@/components/NavBar.vue';

import { useThemePreferences } from '@/composables/useThemePreferences';

const db = useFirestore();
const user = useCurrentUser();

const userDoc = useDocument<TUser>(user.value ? doc(db, 'users', user.value.uid) : null);

const { setTheme } = useThemePreferences();

// Initialize user theme preference
watch([user, userDoc], () => {
  if (userDoc.value?.themePref) {
    let theme = userDoc.value.themePref;

    if (theme === 'system') {
      theme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light';
    }

    setTheme(theme);
  } else {
    setTheme('system');
  }
});
</script>

<template>
  <header id="header">
    <NavBar />
  </header>

  <main id="body">
    <RouterView />
  </main>
</template>

<style scoped>
#header {
  height: 10vh;
}

#body {
  height: 90vh;
}
</style>
