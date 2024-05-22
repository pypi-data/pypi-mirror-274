<template>
  <v-chip v-bind="$attrs" v-on="$listeners">
    <v-avatar left>
      {{ count }}
    </v-avatar>
    <slot />
  </v-chip>
</template>

<script>
export default {
  name: "CounterChip",
  extends: "v-chip",
  props: {
    count: {
      type: Number,
      required: true,
    },
  },
};
</script>
