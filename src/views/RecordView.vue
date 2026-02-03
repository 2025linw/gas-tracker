<script setup lang="ts">
import { collection } from 'firebase/firestore';
import { useCollection, useCurrentUser, useFirestore } from 'vuefire';

import type { TRecord } from '@/types';
import RecordCard from '@/components/RecordCard.vue';

const auth = useCurrentUser();
const db = useFirestore();

const recordsRef = auth.value ? collection(db, 'users', auth.value.uid, 'receipts') : null;
const recordCol = useCollection<TRecord>(recordsRef);
</script>

<template>
  <h1 class="title">This is the records page</h1>

  <div>
    <RecordCard v-for="record in recordCol" :key="record.id" :data="record" />
  </div>
</template>
