<template>
  <cross-reference-selection
    :label="label"
    :value="value"
    @input="bubbleInput"
    @open-modal="openModal" required>

    <generic-edit-modal
      endpoint="api/person"
      :is-visible="isModalVisible"
      @close="closeModal">

      <template slot-scope="{ commit, discard }">
        <modal-person
          :initial="value"
          :commit="commit"
          :discard="discard">
        </modal-person>
      </template>
    </generic-edit-modal>
  </cross-reference-selection>
</template>

<script>
import CrossReferenceSelection from '../../utility/CrossReferenceSelection'
import GenericEditModal from '../GenericEditModal'
import ModalPerson from '../modal_forms/ModalPerson'

export default {
  name: "SelectionPerson",
  components: { CrossReferenceSelection, GenericEditModal, ModalPerson },
  props: {
    value: Object,
    label: {
      type: String,
      default: "Person:"
    }
  },
  data() {
    return {
      isModalVisible: false,
    }
  },
  methods: {
    openModal() {
      this.isModalVisible = true;
    },
    closeModal(selectedObj) {
      this.isModalVisible = false;

      if(selectedObj !== null) {
        this.bubbleInput(selectedObj);
      }
    },
    bubbleInput(obj) {
      this.$emit("input", obj);
    }
  }
}
</script>

<style>

</style>
