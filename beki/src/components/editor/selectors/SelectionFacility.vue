<template>
  <cross-reference-selection
    label="Objekt:"
    :value="value"
    @input="bubbleInput"
    @open-modal="openModal" required>

    <generic-edit-modal
      endpoint="api/facility"
      :is-visible="isModalVisible"
      @close="closeModal">

      <template slot-scope="{ commit, discard }">
        <modal-facility
          :initial="value"
          :commit="commit"
          :discard="discard">
        </modal-facility>
      </template>
    </generic-edit-modal>
  </cross-reference-selection>
</template>

<script>
import CrossReferenceSelection from '../../utility/CrossReferenceSelection'
import GenericEditModal from '../GenericEditModal'
import ModalFacility from '../modal_forms/ModalFacility'

export default {
  name: "SelectionFacility",
  components: { CrossReferenceSelection, GenericEditModal, ModalFacility },
  props: {
    value: Object
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
