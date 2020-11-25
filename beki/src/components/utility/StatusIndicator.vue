<template>
  <nav class="level">
    <div class="level-left">
      <slot></slot>
    </div>
    <div class="level-right">
      <div class="level-item">
        <b-tag :type="type">
            {{ content }}
        </b-tag>
      </div>
    </div>
  </nav>
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
