<template>
  <b-modal
    :active="isVisible"
    has-modal-card
    trap-focus
    :destroy-on-hide="true"
    aria-role="dialog"
    aria-modal>
      <b-loading v-if="isLoading" v-model="isLoading" :is-full-page="false" :can-cancel="false"></b-loading>
      <template v-else>
        <slot :commit="commit" :discard="discard"></slot>
      </template>
  </b-modal>
</template>

<script>
export default {
  name: "GenericEditModal",
  props: {
    endpoint: String,
    isVisible: Boolean
  },
  data() {
    return {
      isLoading: false,
    }
  },
  methods: {
    commit(obj) {
      this.isLoading = true;
      setTimeout(() => {
        console.log("Committed ", JSON.stringify(obj), "to ", this.endpoint);
        this.$emit("close", obj);
        this.isLoading = false;
      }, 1000)
    },
    discard(obj) {
      console.log("Discarding to initial value", obj);
      this.$emit("close", obj);
    }
  }
}
</script>

<style>

</style>
