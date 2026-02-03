<script setup lang="ts">
import type { TRecord } from '@/types';

type Props = {
  data: TRecord;
};
const props = defineProps<Props>();
</script>

<template>
  <main>
    <p>Date: {{ props.data.filledAt.toDate().toLocaleDateString() }}</p>
    <p>Gallons: {{ props.data.gallons }}</p>
    <p>Price Per Gallon: {{ props.data.pricePerGallon }}</p>
    <p>Total: {{ props.data.totalCost }}</p>
  </main>
</template>
