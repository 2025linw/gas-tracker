import { computed, ref, watch } from 'vue';
import { useCurrentUser, useDocument, useFirestore } from 'vuefire';

import type { TThemeOptions, TUser } from '@/types';
import { doc, updateDoc } from 'firebase/firestore';

export function useThemePreferences() {
  const theme = ref<TThemeOptions>('system');

  const user = useCurrentUser();
  const db = useFirestore();

  const userDocRef = computed(() => (user.value ? doc(db, 'users', user.value.uid) : null));
  const userDoc = useDocument<TUser>(userDocRef);
  watch(
    () => userDoc.value?.themePref,
    (value) => {
      if (value) theme.value = value as TThemeOptions;
    },
  );

  watch(theme, (value) => {
    const htmlDataset = document.documentElement.dataset;

    if (value === 'system') delete htmlDataset.theme;
    else htmlDataset.theme = value;

    if (user.value) {
      updateDoc(doc(db, 'users', user.value.uid), {
        themePref: value,
      });
    }
  });

  const setTheme = function (value: TThemeOptions) {
    theme.value = value;
  };

  return { theme, setTheme };
}
