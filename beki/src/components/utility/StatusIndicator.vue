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
          <b-icon v-if="isErr" size="is-small" icon="exclamation-triangle"></b-icon>
          <b-icon v-else-if="isSucc" size="is-small" icon="cloud-upload-alt"></b-icon>
          <b-icon v-else-if="isAwaiting" size="is-small" icon="eye"></b-icon>
          <b-icon v-else-if="isNew" size="is-small" icon="asterisk"></b-icon>
        </b-tag>
      </div>
    </div>
  </div>
</template>

<script>
import { SyncStatus } from '../../store/common';
export default {
  name: "StatusIndicator",
  props: {
    status: Number
  },
  computed: {
    type() {
      if (this.isErr) {
        return 'is-danger';
      }
      if (this.isAwaiting) {
        return 'is-dark';
      }
      if (this.isNew || (this.status & SyncStatus.Modified)) {
        return 'is-warning'
      }
      return 'is-success';
    },
    isErr() {
      return (this.status & SyncStatus.Error) !== 0;
    },
    isSucc() {
      return (this.status & SyncStatus.Stored) !== 0;
    },
    isAwaiting() {
      return (this.status & SyncStatus.AwaitsConfirmation) !== 0;
    },
    isNew() {
      return (this.status & SyncStatus.New) !== 0;
    },
  }
}
</script>

<style>

</style>
