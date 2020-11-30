<template>
  <div class="columns is-gapless">
    <div class="column is-6">
      <div class="level-item is-pulled-left">
      <slot></slot>
      </div>
    </div>
    <div class="column">
      <slot name="center"></slot>
    </div>
    <div class="column">
      <div class="level-item is-pulled-right">
        <b-tag :type="type">
            {{ content }}
        </b-tag>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "StatusIndicator",
  props: {
    status: Number
  },
  computed: {
    type() {
      // TODO: build based on status
      return "is-warning";
    },
    content() {
      // TODO: build based on status
      return "Status"
    }
  }
}
</script>

<style>

</style>
