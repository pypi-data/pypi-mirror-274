<template>
  <orbit-i-o />
  <orbit-shell />
</template>

<script>
import { defineComponent } from 'vue';

import { OrbitIO } from 'orbit-component-base';
import OrbitShell from 'orbit-component-shell';

export default defineComponent({
  components: {OrbitIO, OrbitShell}
})
</script>