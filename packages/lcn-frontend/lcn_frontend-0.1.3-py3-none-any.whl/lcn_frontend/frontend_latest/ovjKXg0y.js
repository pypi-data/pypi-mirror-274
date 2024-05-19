export const id=527;export const ids=[527];export const modules={2218:(e,t,i)=>{i.d(t,{D:()=>a});const a=(e,t,i=!1)=>{let a;const n=(...n)=>{const l=i&&!a;clearTimeout(a),a=window.setTimeout((()=>{a=void 0,i||e(...n)}),t),l&&e(...n)};return n.cancel=()=>{clearTimeout(a)},n}},4376:(e,t,i)=>{var a=i(309),n=i(8417),l=i(9274),o=i(8144),s=i(4243);(0,a.Z)([(0,s.Mo)("ha-checkbox")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[l.W,o.iv`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `]}}]}}),n.A)},9828:(e,t,i)=>{i.d(t,{i:()=>h});var a=i(309),n=i(4541),l=i(7838),o=i(7762),s=i(1632),d=i(8144),r=i(4243),c=i(625);i(4371);const u=["button","ha-list-item"],h=(e,t)=>{var i;return d.dy`
  <div class="header_title">${t}</div>
  <ha-icon-button
    .label=${null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close"}
    .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
    dialogAction="close"
    class="header_button"
  ></ha-icon-button>
`};(0,a.Z)([(0,r.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:c.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return d.dy`<slot name="heading"> ${(0,n.Z)((0,l.Z)(i.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,n.Z)((0,l.Z)(i.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,u].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,n.Z)((0,l.Z)(i.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value(){return[s.W,d.iv`
      :host([scrolled]) ::slotted(ha-dialog-header) {
        border-bottom: 1px solid
          var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
      }
      .mdc-dialog {
        --mdc-dialog-scroll-divider-color: var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );
        z-index: var(--dialog-z-index, 8);
        -webkit-backdrop-filter: var(--dialog-backdrop-filter, none);
        backdrop-filter: var(--dialog-backdrop-filter, none);
        --mdc-dialog-box-shadow: var(--dialog-box-shadow, none);
        --mdc-typography-headline6-font-weight: 400;
        --mdc-typography-headline6-font-size: 1.574rem;
      }
      .mdc-dialog__actions {
        justify-content: var(--justify-action-buttons, flex-end);
        padding-bottom: max(env(safe-area-inset-bottom), 24px);
      }
      .mdc-dialog__actions span:nth-child(1) {
        flex: var(--secondary-action-button-flex, unset);
      }
      .mdc-dialog__actions span:nth-child(2) {
        flex: var(--primary-action-button-flex, unset);
      }
      .mdc-dialog__container {
        align-items: var(--vertical-align-dialog, center);
      }
      .mdc-dialog__title {
        padding: 24px 24px 0 24px;
        text-overflow: ellipsis;
        overflow: hidden;
      }
      .mdc-dialog__actions {
        padding: 12px 24px 12px 24px;
      }
      .mdc-dialog__title::before {
        display: block;
        height: 0px;
      }
      .mdc-dialog .mdc-dialog__content {
        position: var(--dialog-content-position, relative);
        padding: var(--dialog-content-padding, 24px);
      }
      :host([hideactions]) .mdc-dialog .mdc-dialog__content {
        padding-bottom: max(
          var(--dialog-content-padding, 24px),
          env(safe-area-inset-bottom)
        );
      }
      .mdc-dialog .mdc-dialog__surface {
        position: var(--dialog-surface-position, relative);
        top: var(--dialog-surface-top);
        margin-top: var(--dialog-surface-margin-top);
        min-height: var(--mdc-dialog-min-height, auto);
        border-radius: var(--ha-dialog-border-radius, 28px);
      }
      :host([flexContent]) .mdc-dialog .mdc-dialog__content {
        display: flex;
        flex-direction: column;
      }
      .header_title {
        margin-right: 32px;
        margin-inline-end: 32px;
        margin-inline-start: initial;
        direction: var(--direction);
      }
      .header_button {
        position: absolute;
        right: 16px;
        top: 14px;
        text-decoration: none;
        color: inherit;
        inset-inline-start: initial;
        inset-inline-end: 16px;
        direction: var(--direction);
      }
      .dialog-actions {
        inset-inline-start: initial !important;
        inset-inline-end: 0px !important;
        direction: var(--direction);
      }
    `]}}]}}),o.M)},8950:(e,t,i)=>{var a=i(309),n=i(8485),l=i(2038),o=i(8144),s=i(4243),d=i(8394);(0,a.Z)([(0,s.Mo)("ha-formfield")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"_labelClick",value:function(){const e=this.input;if(e&&(e.focus(),!e.disabled))switch(e.tagName){case"HA-CHECKBOX":e.checked=!e.checked,(0,d.B)(e,"change");break;case"HA-RADIO":e.checked=!0,(0,d.B)(e,"change");break;default:e.click()}}},{kind:"field",static:!0,key:"styles",value(){return[l.W,o.iv`
      :host(:not([alignEnd])) ::slotted(ha-switch) {
        margin-right: 10px;
        margin-inline-end: 10px;
        margin-inline-start: inline;
      }
      .mdc-form-field > label {
        direction: var(--direction);
        margin-inline-start: 0;
        margin-inline-end: auto;
        padding-inline-start: 4px;
        padding-inline-end: 0;
      }
    `]}}]}}),n.a)},532:(e,t,i)=>{var a=i(309),n=i(4541),l=i(7838),o=i(1092),s=i(6762),d=i(8144),r=i(4243);(0,a.Z)([(0,r.Mo)("ha-list-item")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"renderRipple",value:function(){return this.noninteractive?"":(0,n.Z)((0,l.Z)(i.prototype),"renderRipple",this).call(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[s.W,d.iv`
        :host {
          padding-left: var(
            --mdc-list-side-padding-left,
            var(--mdc-list-side-padding, 20px)
          );
          padding-right: var(
            --mdc-list-side-padding-right,
            var(--mdc-list-side-padding, 20px)
          );
        }
        :host([graphic="avatar"]:not([twoLine])),
        :host([graphic="icon"]:not([twoLine])) {
          height: 48px;
        }
        span.material-icons:first-of-type {
          margin-inline-start: 0px !important;
          margin-inline-end: var(
            --mdc-list-item-graphic-margin,
            16px
          ) !important;
          direction: var(--direction);
        }
        span.material-icons:last-of-type {
          margin-inline-start: auto !important;
          margin-inline-end: 0px !important;
          direction: var(--direction);
        }
        .mdc-deprecated-list-item__meta {
          display: var(--mdc-list-item-meta-display);
          align-items: center;
        }
        :host([multiline-secondary]) {
          height: auto;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__text {
          padding: 8px 0;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__secondary-text {
          text-overflow: initial;
          white-space: normal;
          overflow: auto;
          display: inline-block;
          margin-top: 10px;
        }
        :host([multiline-secondary]) .mdc-deprecated-list-item__primary-text {
          margin-top: 10px;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__secondary-text::before {
          display: none;
        }
        :host([multiline-secondary])
          .mdc-deprecated-list-item__primary-text::before {
          display: none;
        }
        :host([disabled]) {
          color: var(--disabled-text-color);
        }
        :host([noninteractive]) {
          pointer-events: unset;
        }
      `]}}]}}),o.K)},9096:(e,t,i)=>{var a=i(309),n=i(7463),l=i(4973),o=i(8144),s=i(4243);(0,a.Z)([(0,s.Mo)("ha-radio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",static:!0,key:"styles",value(){return[l.W,o.iv`
      :host {
        --mdc-theme-secondary: var(--primary-color);
      }
    `]}}]}}),n.J)},1133:(e,t,i)=>{var a=i(309),n=i(4541),l=i(7838),o=i(2933),s=i(3762),d=i(8144),r=i(4243),c=i(2218),u=i(2537);i(4371);(0,a.Z)([(0,r.Mo)("ha-select")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"icon",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"clearable",value:void 0},{kind:"method",key:"render",value:function(){return d.dy`
      ${(0,n.Z)((0,l.Z)(i.prototype),"render",this).call(this)}
      ${this.clearable&&!this.required&&!this.disabled&&this.value?d.dy`<ha-icon-button
            label="clear"
            @click=${this._clearValue}
            .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
          ></ha-icon-button>`:d.Ld}
    `}},{kind:"method",key:"renderLeadingIcon",value:function(){return this.icon?d.dy`<span class="mdc-select__icon"
      ><slot name="icon"></slot
    ></span>`:d.Ld}},{kind:"method",key:"connectedCallback",value:function(){(0,n.Z)((0,l.Z)(i.prototype),"connectedCallback",this).call(this),window.addEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"disconnectedCallback",value:function(){(0,n.Z)((0,l.Z)(i.prototype),"disconnectedCallback",this).call(this),window.removeEventListener("translations-updated",this._translationsUpdated)}},{kind:"method",key:"_clearValue",value:function(){!this.disabled&&this.value&&(this.valueSetDirectly=!0,this.select(-1),this.mdcFoundation.handleChange())}},{kind:"field",key:"_translationsUpdated",value(){return(0,c.D)((async()=>{await(0,u.y)(),this.layoutOptions()}),500)}},{kind:"field",static:!0,key:"styles",value(){return[s.W,d.iv`
      :host([clearable]) {
        position: relative;
      }
      .mdc-select:not(.mdc-select--disabled) .mdc-select__icon {
        color: var(--secondary-text-color);
      }
      .mdc-select__anchor {
        width: var(--ha-select-min-width, 200px);
      }
      .mdc-select--filled .mdc-select__anchor {
        height: var(--ha-select-height, 56px);
      }
      .mdc-select--filled .mdc-floating-label {
        inset-inline-start: 12px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select--filled.mdc-select--with-leading-icon .mdc-floating-label {
        inset-inline-start: 48px;
        inset-inline-end: initial;
        direction: var(--direction);
      }
      .mdc-select .mdc-select__anchor {
        padding-inline-start: 12px;
        padding-inline-end: 0px;
        direction: var(--direction);
      }
      .mdc-select__anchor .mdc-floating-label--float-above {
        transform-origin: var(--float-start);
      }
      .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 0px);
      }
      :host([clearable]) .mdc-select__selected-text-container {
        padding-inline-end: var(--select-selected-text-padding-end, 12px);
      }
      ha-icon-button {
        position: absolute;
        top: 10px;
        right: 28px;
        --mdc-icon-button-size: 36px;
        --mdc-icon-size: 20px;
        color: var(--secondary-text-color);
        inset-inline-start: initial;
        inset-inline-end: 28px;
        direction: var(--direction);
      }
    `]}}]}}),o.K)},3638:(e,t,i)=>{var a=i(309),n=i(4541),l=i(7838),o=i(3464),s=i(4301),d=i(8144),r=i(4243),c=i(8394);(0,a.Z)([(0,r.Mo)("ha-switch")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"haptic",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(){(0,n.Z)((0,l.Z)(i.prototype),"firstUpdated",this).call(this),this.addEventListener("change",(()=>{var e;this.haptic&&(e="light",(0,c.B)(window,"haptic",e))}))}},{kind:"field",static:!0,key:"styles",value(){return[s.W,d.iv`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `]}}]}}),o.H)},1520:(e,t,i)=>{var a=i(309),n=i(4541),l=i(7838),o=i(6437),s=i(1338),d=i(8144),r=i(4243),c=i(2138);(0,a.Z)([(0,r.Mo)("ha-textfield")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"invalid",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:"error-message"})],key:"errorMessage",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"icon",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"iconTrailing",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"autocomplete",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"autocorrect",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:"input-spellcheck"})],key:"inputSpellcheck",value:void 0},{kind:"field",decorators:[(0,r.IO)("input")],key:"formElement",value:void 0},{kind:"method",key:"updated",value:function(e){(0,n.Z)((0,l.Z)(i.prototype),"updated",this).call(this,e),(e.has("invalid")&&(this.invalid||void 0!==e.get("invalid"))||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||"Invalid":""),this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(this.autocorrect?this.formElement.setAttribute("autocorrect",this.autocorrect):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}},{kind:"method",key:"renderIcon",value:function(e,t=!1){const i=t?"trailing":"leading";return d.dy`
      <span
        class="mdc-text-field__icon mdc-text-field__icon--${i}"
        tabindex=${t?1:-1}
      >
        <slot name="${i}Icon"></slot>
      </span>
    `}},{kind:"field",static:!0,key:"styles",value(){return[s.W,d.iv`
      .mdc-text-field__input {
        width: var(--ha-textfield-input-width, 100%);
      }
      .mdc-text-field:not(.mdc-text-field--with-leading-icon) {
        padding: var(--text-field-padding, 0px 16px);
      }
      .mdc-text-field__affix--suffix {
        padding-left: var(--text-field-suffix-padding-left, 12px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 12px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
        direction: var(--direction);
      }
      .mdc-text-field--with-leading-icon {
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 16px);
        direction: var(--direction);
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon {
        padding-left: var(--text-field-suffix-padding-left, 0px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
      }
      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--suffix {
        color: var(--secondary-text-color);
      }

      .mdc-text-field__icon {
        color: var(--secondary-text-color);
      }

      .mdc-text-field__icon--leading {
        margin-inline-start: 16px;
        margin-inline-end: 8px;
        direction: var(--direction);
      }

      .mdc-text-field__icon--trailing {
        padding: var(--textfield-icon-trailing-padding, 12px);
      }

      .mdc-floating-label:not(.mdc-floating-label--float-above) {
        text-overflow: ellipsis;
        width: inherit;
        padding-right: 30px;
        padding-inline-end: 30px;
        padding-inline-start: initial;
        box-sizing: border-box;
        direction: var(--direction);
      }

      input {
        text-align: var(--text-field-text-align, start);
      }

      /* Edge, hide reveal password icon */
      ::-ms-reveal {
        display: none;
      }

      /* Chrome, Safari, Edge, Opera */
      :host([no-spinner]) input::-webkit-outer-spin-button,
      :host([no-spinner]) input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }

      /* Firefox */
      :host([no-spinner]) input[type="number"] {
        -moz-appearance: textfield;
      }

      .mdc-text-field__ripple {
        overflow: hidden;
      }

      .mdc-text-field {
        overflow: var(--text-field-overflow);
      }

      .mdc-floating-label {
        inset-inline-start: 16px !important;
        inset-inline-end: initial !important;
        transform-origin: var(--float-start);
        direction: var(--direction);
        text-align: var(--float-start);
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--filled
        .mdc-floating-label {
        max-width: calc(
          100% - 48px - var(--text-field-suffix-padding-left, 0px)
        );
        inset-inline-start: calc(
          48px + var(--text-field-suffix-padding-left, 0px)
        ) !important;
        inset-inline-end: initial !important;
        direction: var(--direction);
      }

      .mdc-text-field__input[type="number"] {
        direction: var(--direction);
      }
      .mdc-text-field__affix--prefix {
        padding-right: var(--text-field-prefix-padding-right, 2px);
      }

      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--prefix {
        color: var(--mdc-text-field-label-ink-color);
      }
    `,"rtl"===c.E.document.dir?d.iv`
          .mdc-text-field__affix--suffix,
          .mdc-text-field--with-leading-icon,
          .mdc-text-field__icon--leading,
          .mdc-floating-label,
          .mdc-text-field--with-leading-icon.mdc-text-field--filled
            .mdc-floating-label,
          .mdc-text-field__input[type="number"] {
            direction: rtl;
          }
        `:d.iv``]}}]}}),o.P)},1285:(e,t,i)=>{i.d(t,{Ys:()=>o,g7:()=>s});var a=i(8394);const n=()=>Promise.all([i.e(597),i.e(338)]).then(i.bind(i,4338)),l=(e,t,i)=>new Promise((l=>{const o=t.cancel,s=t.confirm;(0,a.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:n,dialogParams:{...t,...i,cancel:()=>{l(!(null==i||!i.prompt)&&null),o&&o()},confirm:e=>{l(null==i||!i.prompt||e),s&&s(e)}}})})),o=(e,t)=>l(e,t),s=(e,t)=>l(e,t,{confirmation:!0})},6527:(e,t,i)=>{i.r(t),i.d(t,{CreateEntityDialog:()=>m});var a=i(309),n=(i(4371),i(532),i(1133),i(8394)),l=i(8144),o=i(4243),s=i(9828);const d=e=>e.stopPropagation();var r=i(9950),c=i(4541),u=i(7838);(0,a.Z)([(0,o.Mo)("lcn-config-binary-sensor-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"domainData",value(){return{source:"BINSENSOR1"}}},{kind:"field",decorators:[(0,o.SB)()],key:"_sourceType",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,o.IO)("#source-select")],key:"_sourceSelect",value:void 0},{kind:"get",key:"_binsensorPorts",value:function(){const e=this.lcn.localize("binary-sensor");return[{name:e+" 1",value:"BINSENSOR1"},{name:e+" 2",value:"BINSENSOR2"},{name:e+" 3",value:"BINSENSOR3"},{name:e+" 4",value:"BINSENSOR4"},{name:e+" 5",value:"BINSENSOR5"},{name:e+" 6",value:"BINSENSOR6"},{name:e+" 7",value:"BINSENSOR7"},{name:e+" 8",value:"BINSENSOR8"}]}},{kind:"get",key:"_setpoints",value:function(){const e=this.lcn.localize("setpoint");return[{name:e+" 1",value:"R1VARSETPOINT"},{name:e+" 2",value:"R2VARSETPOINT"}]}},{kind:"field",key:"_keys",value(){return[{name:"A1",value:"A1"},{name:"A2",value:"A2"},{name:"A3",value:"A3"},{name:"A4",value:"A4"},{name:"A5",value:"A5"},{name:"A6",value:"A6"},{name:"A7",value:"A7"},{name:"A8",value:"A8"},{name:"B1",value:"B1"},{name:"B2",value:"B2"},{name:"B3",value:"B3"},{name:"B4",value:"B4"},{name:"B5",value:"B5"},{name:"B6",value:"B6"},{name:"B7",value:"B7"},{name:"B8",value:"B8"},{name:"C1",value:"C1"},{name:"C2",value:"C2"},{name:"C3",value:"C3"},{name:"C4",value:"C4"},{name:"C5",value:"C5"},{name:"C6",value:"C6"},{name:"C7",value:"C7"},{name:"C8",value:"C8"},{name:"D1",value:"D1"},{name:"D2",value:"D2"},{name:"D3",value:"D3"},{name:"D4",value:"D4"},{name:"D5",value:"D5"},{name:"D6",value:"D6"},{name:"D7",value:"D7"},{name:"D8",value:"D8"}]}},{kind:"get",key:"_sourceTypes",value:function(){return[{name:this.lcn.localize("binary-sensor-type-binsensors"),value:this._binsensorPorts,id:"binsensors"},{name:this.lcn.localize("binary-sensor-type-setpoint-locks"),value:this._setpoints,id:"setpoint-locks"},{name:this.lcn.localize("binary-sensor-type-keys-locks"),value:this._keys,id:"key-locks"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,u.Z)(i.prototype),"connectedCallback",this).call(this),this._sourceType=this._sourceTypes[0],this._source=this._sourceType.value[0]}},{kind:"method",key:"render",value:function(){return this._sourceType||this._source?l.dy`
      <div class="sources">
        <ha-select
          id="source-type-select"
          .label=${this.lcn.localize("source-type")}
          .value=${this._sourceType.id}
          fixedMenuPosition
          @selected=${this._sourceTypeChanged}
          @closed=${d}
        >
          ${this._sourceTypes.map((e=>l.dy`
              <ha-list-item .value=${e.id}> ${e.name} </ha-list-item>
            `))}
        </ha-select>

        <ha-select
          id="source-select"
          .label=${this.lcn.localize("source")}
          .value=${this._source.value}
          fixedMenuPosition
          @selected=${this._sourceChanged}
          @closed=${d}
        >
          ${this._sourceType.value.map((e=>l.dy`
              <ha-list-item .value=${e.value}> ${e.name} </ha-list-item>
            `))}
        </ha-select>
      </div>
    `:l.Ld}},{kind:"method",key:"_sourceTypeChanged",value:function(e){const t=e.target;-1!==t.index&&(this._sourceType=this._sourceTypes.find((e=>e.id===t.value)),this._source=this._sourceType.value[0],this._sourceSelect.select(-1))}},{kind:"method",key:"_sourceChanged",value:function(e){const t=e.target;-1!==t.index&&(this._source=this._sourceType.value.find((e=>e.value===t.value)),this.domainData.source=this._source.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        .sources {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `]}}]}}),l.oi);i(1520),i(3638);(0,a.Z)([(0,o.Mo)("lcn-config-climate-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Number})],key:"softwareSerial",value(){return-1}},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"domainData",value(){return{source:"VAR1",setpoint:"R1VARSETPOINT",max_temp:35,min_temp:7,lockable:!1,unit_of_measurement:"°C"}}},{kind:"field",decorators:[(0,o.SB)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_setpoint",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_unit",value:void 0},{kind:"field",key:"_invalid",value(){return!1}},{kind:"get",key:"_is2012",value:function(){return this.softwareSerial>=1441792}},{kind:"get",key:"_variablesNew",value:function(){const e=this.lcn.localize("variable");return[{name:e+" 1",value:"VAR1"},{name:e+" 2",value:"VAR2"},{name:e+" 3",value:"VAR3"},{name:e+" 4",value:"VAR4"},{name:e+" 5",value:"VAR5"},{name:e+" 6",value:"VAR6"},{name:e+" 7",value:"VAR7"},{name:e+" 8",value:"VAR8"},{name:e+" 9",value:"VAR9"},{name:e+" 10",value:"VAR10"},{name:e+" 11",value:"VAR11"},{name:e+" 12",value:"VAR12"}]}},{kind:"field",key:"_variablesOld",value(){return[{name:"TVar",value:"TVAR"},{name:"R1Var",value:"R1VAR"},{name:"R2Var",value:"R2VAR"}]}},{kind:"get",key:"_varSetpoints",value:function(){const e=this.lcn.localize("setpoint");return[{name:e+" 1",value:"R1VARSETPOINT"},{name:e+" 2",value:"R2VARSETPOINT"}]}},{kind:"field",key:"_varUnits",value(){return[{name:"Celsius",value:"°C"},{name:"Fahrenheit",value:"°F"}]}},{kind:"get",key:"_sources",value:function(){return this._is2012?this._variablesNew:this._variablesOld}},{kind:"get",key:"_setpoints",value:function(){return this._is2012?this._varSetpoints.concat(this._variablesNew):this._varSetpoints}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,u.Z)(i.prototype),"connectedCallback",this).call(this),this._source=this._sources[0],this._setpoint=this._setpoints[0],this._unit=this._varUnits[0]}},{kind:"method",key:"willUpdate",value:function(e){(0,c.Z)((0,u.Z)(i.prototype),"willUpdate",this).call(this,e),this._invalid=!this._validateMinTemp(this.domainData.min_temp)||!this._validateMaxTemp(this.domainData.max_temp)}},{kind:"method",key:"update",value:function(e){(0,c.Z)((0,u.Z)(i.prototype),"update",this).call(this,e),this.dispatchEvent(new CustomEvent("validity-changed",{detail:this._invalid,bubbles:!0,composed:!0}))}},{kind:"method",key:"render",value:function(){return this._source||this._setpoint||this._unit?l.dy`
      <div class="sources">
        <ha-select
          id="source-select"
          .label=${this.lcn.localize("source")}
          .value=${this._source.value}
          fixedMenuPosition
          @selected=${this._sourceChanged}
          @closed=${d}
        >
          ${this._sources.map((e=>l.dy`
              <ha-list-item .value=${e.value}> ${e.name} </ha-list-item>
            `))}
        </ha-select>

        <ha-select
          id="setpoint-select"
          .label=${this.lcn.localize("setpoint")}
          .value=${this._setpoint.value}
          fixedMenuPosition
          @selected=${this._setpointChanged}
          @closed=${d}
        >
          ${this._setpoints.map((e=>l.dy`
              <ha-list-item .value=${e.value}> ${e.name} </ha-list-item>
            `))}
        </ha-select>
      </div>

      <div class="lockable">
        <label>${this.lcn.localize("dashboard-entities-dialog-climate-lockable")}:</label>
        <ha-switch
          .checked=${this.domainData.lockable}
          @change=${this._lockableChanged}
        ></ha-switch>
      </div>

      <ha-textfield
        id="min-textfield"
        .label=${this.lcn.localize("dashboard-entities-dialog-climate-min-temperature")}
        type="number"
        .value=${this.domainData.min_temp.toString()}
        required
        autoValidate
        @input=${this._minTempChanged}
        .validityTransform=${this._validityTransformMinTemp}
        .validationMessage=${this.lcn.localize("dashboard-entities-dialog-climate-min-temperature-error")}
      ></ha-textfield>

      <ha-textfield
        id="max-textfield"
        .label=${this.lcn.localize("dashboard-entities-dialog-climate-max-temperature")}
        type="number"
        .value=${this.domainData.max_temp.toString()}
        required
        autoValidate
        @input=${this._maxTempChanged}
        .validityTransform=${this._validityTransformMaxTemp}
        .validationMessage=${this.lcn.localize("dashboard-entities-dialog-climate-max-temperature-error")}
      ></ha-textfield>

      <ha-select
        id="unit-select"
        .label=${this.lcn.localize("dashboard-entities-dialog-unit-of-measurement")}
        .value=${this._unit.value}
        fixedMenuPosition
        @selected=${this._unitChanged}
        @closed=${d}
      >
        ${this._varUnits.map((e=>l.dy` <ha-list-item .value=${e.value}> ${e.name} </ha-list-item> `))}
      </ha-select>
    `:l.Ld}},{kind:"method",key:"_sourceChanged",value:function(e){const t=e.target;-1!==t.index&&(this._source=this._sources.find((e=>e.value===t.value)),this.domainData.source=this._source.value)}},{kind:"method",key:"_setpointChanged",value:function(e){const t=e.target;-1!==t.index&&(this._setpoint=this._setpoints.find((e=>e.value===t.value)),this.domainData.setpoint=this._setpoint.value)}},{kind:"method",key:"_minTempChanged",value:function(e){const t=e.target;this.domainData.min_temp=+t.value;this.shadowRoot.querySelector("#max-textfield").reportValidity(),this.requestUpdate()}},{kind:"method",key:"_maxTempChanged",value:function(e){const t=e.target;this.domainData.max_temp=+t.value;this.shadowRoot.querySelector("#min-textfield").reportValidity(),this.requestUpdate()}},{kind:"method",key:"_lockableChanged",value:function(e){this.domainData.lockable=e.target.checked}},{kind:"method",key:"_unitChanged",value:function(e){const t=e.target;-1!==t.index&&(this._unit=this._varUnits.find((e=>e.value===t.value)),this.domainData.unit_of_measurement=this._unit.value)}},{kind:"method",key:"_validateMaxTemp",value:function(e){return e>this.domainData.min_temp}},{kind:"method",key:"_validateMinTemp",value:function(e){return e<this.domainData.max_temp}},{kind:"get",key:"_validityTransformMaxTemp",value:function(){return e=>({valid:this._validateMaxTemp(+e)})}},{kind:"get",key:"_validityTransformMinTemp",value:function(){return e=>({valid:this._validateMinTemp(+e)})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        .sources {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        .lockable {
          margin-top: 10px;
        }
        ha-switch {
          margin-left: 25px;
        }
      `]}}]}}),l.oi);i(7221),i(3507),i(2943);(0,a.Z)([(0,o.Mo)("lcn-config-cover-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"domainData",value(){return{motor:"MOTOR1",reverse_time:"RT1200"}}},{kind:"field",decorators:[(0,o.SB)()],key:"_motor",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_reverseDelay",value:void 0},{kind:"get",key:"_motors",value:function(){const e=this.lcn.localize("motor");return[{name:e+" 1",value:"MOTOR1"},{name:e+" 2",value:"MOTOR2"},{name:e+" 3",value:"MOTOR3"},{name:e+" 4",value:"MOTOR4"},{name:this.lcn.localize("outputs"),value:"OUTPUTS"}]}},{kind:"field",key:"_reverseDelays",value(){return[{name:"70ms",value:"RT70"},{name:"600ms",value:"RT600"},{name:"1200ms",value:"RT1200"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,u.Z)(i.prototype),"connectedCallback",this).call(this),this._motor=this._motors[0],this._reverseDelay=this._reverseDelays[0]}},{kind:"method",key:"render",value:function(){return this._motor||this._reverseDelay?l.dy`
      <ha-select
        id="motor-select"
        .label=${this.lcn.localize("motor")}
        .value=${this._motor.value}
        fixedMenuPosition
        @selected=${this._motorChanged}
        @closed=${d}
      >
        ${this._motors.map((e=>l.dy` <ha-list-item .value=${e.value}> ${e.name} </ha-list-item> `))}
      </ha-select>

      ${"OUTPUTS"===this._motor.value?l.dy`
            <ha-select
              id="reverse-delay-select"
              .label=${this.lcn.localize("reverse-delay")}
              .value=${this._reverseDelay.value}
              fixedMenuPosition
              @selected=${this._reverseDelayChanged}
              @closed=${d}
            >
              ${this._reverseDelays.map((e=>l.dy`
                  <ha-list-item .value=${e.value}> ${e.name} </ha-list-item>
                `))}
            </ha-select>
          `:l.Ld}
    `:l.Ld}},{kind:"method",key:"_motorChanged",value:function(e){const t=e.target;-1!==t.index&&(this._motor=this._motors.find((e=>e.value===t.value)),this._reverseDelay=this._reverseDelays[0],this.domainData.motor=this._motor.value)}},{kind:"method",key:"_reverseDelayChanged",value:function(e){const t=e.target;-1!==t.index&&(this._reverseDelay=this._reverseDelays.find((e=>e.value===t.value)),this.domainData.reverse_time=this._reverseDelay.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `]}}]}}),l.oi);i(9096),i(8950);(0,a.Z)([(0,o.Mo)("lcn-config-light-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"domainData",value(){return{output:"OUTPUT1",dimmable:!1,transition:0}}},{kind:"field",decorators:[(0,o.SB)()],key:"_portType",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_port",value:void 0},{kind:"field",decorators:[(0,o.IO)("#port-select")],key:"_portSelect",value:void 0},{kind:"field",key:"_invalid",value(){return!1}},{kind:"get",key:"_outputPorts",value:function(){const e=this.lcn.localize("output");return[{name:e+" 1",value:"OUTPUT1"},{name:e+" 2",value:"OUTPUT2"},{name:e+" 3",value:"OUTPUT3"},{name:e+" 4",value:"OUTPUT4"}]}},{kind:"get",key:"_relayPorts",value:function(){const e=this.lcn.localize("relay");return[{name:e+" 1",value:"RELAY1"},{name:e+" 2",value:"RELAY2"},{name:e+" 3",value:"RELAY3"},{name:e+" 4",value:"RELAY4"},{name:e+" 5",value:"RELAY5"},{name:e+" 6",value:"RELAY6"},{name:e+" 7",value:"RELAY7"},{name:e+" 8",value:"RELAY8"}]}},{kind:"get",key:"_portTypes",value:function(){return[{name:this.lcn.localize("output"),value:this._outputPorts,id:"output"},{name:this.lcn.localize("relay"),value:this._relayPorts,id:"relay"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,u.Z)(i.prototype),"connectedCallback",this).call(this),this._portType=this._portTypes[0],this._port=this._portType.value[0]}},{kind:"method",key:"willUpdate",value:function(e){(0,c.Z)((0,u.Z)(i.prototype),"willUpdate",this).call(this,e),this._invalid=!this._validateTransition(this.domainData.transition)}},{kind:"method",key:"update",value:function(e){(0,c.Z)((0,u.Z)(i.prototype),"update",this).call(this,e),this.dispatchEvent(new CustomEvent("validity-changed",{detail:this._invalid,bubbles:!0,composed:!0}))}},{kind:"method",key:"render",value:function(){return this._portType||this._port?l.dy`
      <div id="port-type">${this.lcn.localize("port-type")}</div>

      <ha-formfield label=${this.lcn.localize("output")}>
        <ha-radio
          name="port"
          value="output"
          .checked=${"output"===this._portType.id}
          @change=${this._portTypeChanged}
        ></ha-radio>
      </ha-formfield>

      <ha-formfield label=${this.lcn.localize("relay")}>
        <ha-radio
          name="port"
          value="relay"
          .checked=${"relay"===this._portType.id}
          @change=${this._portTypeChanged}
        ></ha-radio>
      </ha-formfield>

      <ha-select
        id="port-select"
        .label=${this.lcn.localize("port")}
        .value=${this._port.value}
        fixedMenuPosition
        @selected=${this._portChanged}
        @closed=${d}
      >
        ${this._portType.value.map((e=>l.dy` <ha-list-item .value=${e.value}> ${e.name} </ha-list-item> `))}
      </ha-select>

      ${this.renderOutputFeatures()}
    `:l.Ld}},{kind:"method",key:"renderOutputFeatures",value:function(){return"output"===this._portType.id?l.dy`
          <div id="dimmable">
            <label>${this.lcn.localize("dashboard-entities-dialog-light-dimmable")}:</label>

            <ha-switch
              .checked=${this.domainData.dimmable}
              @change=${this._dimmableChanged}
            ></ha-switch>
          </div>

          <ha-textfield
            id="transition"
            .label=${this.lcn.localize("dashboard-entities-dialog-light-transition")}
            type="number"
            .value=${this.domainData.transition.toString()}
            min="0"
            max="486"
            required
            autoValidate
            @input=${this._transitionChanged}
            .validityTransform=${this._validityTransformTransition}
            .validationMessage=${this.lcn.localize("dashboard-entities-dialog-light-transition-error")}
          ></ha-textfield>
        `:l.Ld}},{kind:"method",key:"_portTypeChanged",value:function(e){const t=e.target;this._portType=this._portTypes.find((e=>e.id===t.value)),this._port=this._portType.value[0],this._portSelect.select(-1)}},{kind:"method",key:"_portChanged",value:function(e){const t=e.target;-1!==t.index&&(this._port=this._portType.value.find((e=>e.value===t.value)),this.domainData.output=this._port.value)}},{kind:"method",key:"_dimmableChanged",value:function(e){this.domainData.dimmable=e.target.checked}},{kind:"method",key:"_transitionChanged",value:function(e){const t=e.target;this.domainData.transition=+t.value,this.requestUpdate()}},{kind:"method",key:"_validateTransition",value:function(e){return e>=0&&e<=486}},{kind:"get",key:"_validityTransformTransition",value:function(){return e=>({valid:this._validateTransition(+e)})}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        #port-type {
          margin-top: 16px;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        #dimmable {
          margin-top: 16px;
        }
        #transition {
          margin-top: 16px;
        }
      `]}}]}}),l.oi);i(4376);(0,a.Z)([(0,o.Mo)("lcn-config-scene-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"domainData",value(){return{register:0,scene:0,outputs:[],transition:0}}},{kind:"field",decorators:[(0,o.SB)()],key:"_register",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_scene",value:void 0},{kind:"field",key:"_invalid",value(){return!1}},{kind:"get",key:"_registers",value:function(){const e=this.lcn.localize("register");return[{name:e+" 0",value:"0"},{name:e+" 1",value:"1"},{name:e+" 2",value:"2"},{name:e+" 3",value:"3"},{name:e+" 4",value:"4"},{name:e+" 5",value:"5"},{name:e+" 6",value:"6"},{name:e+" 7",value:"7"},{name:e+" 8",value:"8"},{name:e+" 9",value:"9"}]}},{kind:"get",key:"_scenes",value:function(){const e=this.lcn.localize("scene");return[{name:e+" 1",value:"0"},{name:e+" 2",value:"1"},{name:e+" 3",value:"2"},{name:e+" 4",value:"3"},{name:e+" 5",value:"4"},{name:e+" 6",value:"5"},{name:e+" 7",value:"6"},{name:e+" 8",value:"7"},{name:e+" 9",value:"8"},{name:e+" 10",value:"9"}]}},{kind:"get",key:"_outputPorts",value:function(){const e=this.lcn.localize("output");return[{name:e+" 1",value:"OUTPUT1"},{name:e+" 2",value:"OUTPUT2"},{name:e+" 3",value:"OUTPUT3"},{name:e+" 4",value:"OUTPUT4"}]}},{kind:"get",key:"_relayPorts",value:function(){const e=this.lcn.localize("relay");return[{name:e+" 1",value:"RELAY1"},{name:e+" 2",value:"RELAY2"},{name:e+" 3",value:"RELAY3"},{name:e+" 4",value:"RELAY4"},{name:e+" 5",value:"RELAY5"},{name:e+" 6",value:"RELAY6"},{name:e+" 7",value:"RELAY7"},{name:e+" 8",value:"RELAY8"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,u.Z)(i.prototype),"connectedCallback",this).call(this),this._register=this._registers[0],this._scene=this._scenes[0]}},{kind:"method",key:"willUpdate",value:function(e){(0,c.Z)((0,u.Z)(i.prototype),"willUpdate",this).call(this,e),this._invalid=!this._validateTransition(this.domainData.transition)}},{kind:"method",key:"update",value:function(e){(0,c.Z)((0,u.Z)(i.prototype),"update",this).call(this,e),this.dispatchEvent(new CustomEvent("validity-changed",{detail:this._invalid,bubbles:!0,composed:!0}))}},{kind:"method",key:"render",value:function(){return this._register||this._scene?l.dy`
      <div class="registers">
        <ha-select
          id="register-select"
          .label=${this.lcn.localize("register")}
          .value=${this._register.value}
          fixedMenuPosition
          @selected=${this._registerChanged}
          @closed=${d}
        >
          ${this._registers.map((e=>l.dy`
              <ha-list-item .value=${e.value}> ${e.name} </ha-list-item>
            `))}
        </ha-select>

        <ha-select
          id="scene-select"
          .label=${this.lcn.localize("scene")}
          .value=${this._scene.value}
          fixedMenuPosition
          @selected=${this._sceneChanged}
          @closed=${d}
        >
          ${this._scenes.map((e=>l.dy` <ha-list-item .value=${e.value}> ${e.name} </ha-list-item> `))}
        </ha-select>
      </div>

      <div class="ports">
        <label>${this.lcn.localize("outputs")}:</label><br />
        ${this._outputPorts.map((e=>l.dy`
            <ha-formfield label=${e.name}>
              <ha-checkbox .value=${e.value} @change=${this._portCheckedChanged}></ha-checkbox>
            </ha-formfield>
          `))}
      </div>

      <div class="ports">
        <label>${this.lcn.localize("relays")}:</label><br />
        ${this._relayPorts.map((e=>l.dy`
            <ha-formfield label=${e.name}>
              <ha-checkbox .value=${e.value} @change=${this._portCheckedChanged}></ha-checkbox>
            </ha-formfield>
          `))}
      </div>

      <ha-textfield
        .label=${this.lcn.localize("dashboard-entities-dialog-scene-transition")}
        type="number"
        .value=${this.domainData.transition.toString()}
        min="0"
        max="486"
        required
        autoValidate
        @input=${this._transitionChanged}
        .validityTransform=${this._validityTransformTransition}
        .disabled=${this._transitionDisabled}
        .validationMessage=${this.lcn.localize("dashboard-entities-dialog-scene-transition-error")}
      ></ha-textfield>
    `:l.Ld}},{kind:"method",key:"_registerChanged",value:function(e){const t=e.target;-1!==t.index&&(this._register=this._registers.find((e=>e.value===t.value)),this.domainData.register=+this._register.value)}},{kind:"method",key:"_sceneChanged",value:function(e){const t=e.target;-1!==t.index&&(this._scene=this._scenes.find((e=>e.value===t.value)),this.domainData.scene=+this._scene.value)}},{kind:"method",key:"_portCheckedChanged",value:function(e){e.target.checked?this.domainData.outputs.push(e.target.value):this.domainData.outputs=this.domainData.outputs.filter((t=>e.target.value!==t)),this.requestUpdate()}},{kind:"method",key:"_transitionChanged",value:function(e){const t=e.target;this.domainData.transition=+t.value,this.requestUpdate()}},{kind:"method",key:"_validateTransition",value:function(e){return e>=0&&e<=486}},{kind:"get",key:"_validityTransformTransition",value:function(){return e=>({valid:this._validateTransition(+e)})}},{kind:"get",key:"_transitionDisabled",value:function(){const e=this._outputPorts.map((e=>e.value));return 0===this.domainData.outputs.filter((t=>e.includes(t))).length}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        .registers {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        .ports {
          margin-top: 10px;
        }
      `]}}]}}),l.oi),(0,a.Z)([(0,o.Mo)("lcn-config-sensor-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Number})],key:"softwareSerial",value(){return-1}},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"domainData",value(){return{source:"VAR1",unit_of_measurement:"NATIVE"}}},{kind:"field",decorators:[(0,o.SB)()],key:"_sourceType",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_source",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_unit",value:void 0},{kind:"field",decorators:[(0,o.IO)("#source-select")],key:"_sourceSelect",value:void 0},{kind:"get",key:"_is2013",value:function(){return this.softwareSerial>=1507846}},{kind:"field",key:"_variablesOld",value(){return[{name:"TVar",value:"TVAR"},{name:"R1Var",value:"R1VAR"},{name:"R2Var",value:"R2VAR"}]}},{kind:"get",key:"_variablesNew",value:function(){const e=this.lcn.localize("variable");return[{name:e+" 1",value:"VAR1"},{name:e+" 2",value:"VAR2"},{name:e+" 3",value:"VAR3"},{name:e+" 4",value:"VAR4"},{name:e+" 5",value:"VAR5"},{name:e+" 6",value:"VAR6"},{name:e+" 7",value:"VAR7"},{name:e+" 8",value:"VAR8"},{name:e+" 9",value:"VAR9"},{name:e+" 10",value:"VAR10"},{name:e+" 11",value:"VAR11"},{name:e+" 12",value:"VAR12"}]}},{kind:"get",key:"_setpoints",value:function(){const e=this.lcn.localize("setpoint");return[{name:e+" 1",value:"R1VARSETPOINT"},{name:e+" 2",value:"R2VARSETPOINT"}]}},{kind:"get",key:"_thresholdsOld",value:function(){const e=this.lcn.localize("threshold");return[{name:e+" 1",value:"THRS1"},{name:e+" 2",value:"THRS2"},{name:e+" 3",value:"THRS3"},{name:e+" 4",value:"THRS4"},{name:e+" 5",value:"THRS5"}]}},{kind:"get",key:"_thresholdsNew",value:function(){const e=this.lcn.localize("threshold");return[{name:e+" 1-1",value:"THRS1"},{name:e+" 1-2",value:"THRS2"},{name:e+" 1-3",value:"THRS3"},{name:e+" 1-4",value:"THRS4"},{name:e+" 2-1",value:"THRS2_1"},{name:e+" 2-2",value:"THRS2_2"},{name:e+" 2-3",value:"THRS2_3"},{name:e+" 2-4",value:"THRS2_4"},{name:e+" 3-1",value:"THRS3_1"},{name:e+" 3-2",value:"THRS3_2"},{name:e+" 3-3",value:"THRS3_3"},{name:e+" 3-4",value:"THRS3_4"},{name:e+" 4-1",value:"THRS4_1"},{name:e+" 4-2",value:"THRS4_2"},{name:e+" 4-3",value:"THRS4_3"},{name:e+" 4-4",value:"THRS4_4"}]}},{kind:"get",key:"_s0Inputs",value:function(){const e=this.lcn.localize("s0input");return[{name:e+" 1",value:"S0INPUT1"},{name:e+" 2",value:"S0INPUT2"},{name:e+" 3",value:"S0INPUT3"},{name:e+" 4",value:"S0INPUT4"}]}},{kind:"get",key:"_ledPorts",value:function(){const e=this.lcn.localize("led");return[{name:e+" 1",value:"LED1"},{name:e+" 2",value:"LED2"},{name:e+" 3",value:"LED3"},{name:e+" 4",value:"LED4"},{name:e+" 5",value:"LED5"},{name:e+" 6",value:"LED6"},{name:e+" 7",value:"LED7"},{name:e+" 8",value:"LED8"},{name:e+" 9",value:"LED9"},{name:e+" 10",value:"LED10"},{name:e+" 11",value:"LED11"},{name:e+" 12",value:"LED12"}]}},{kind:"get",key:"_logicOpPorts",value:function(){const e=this.lcn.localize("logic");return[{name:e+" 1",value:"LOGICOP1"},{name:e+" 2",value:"LOGICOP2"},{name:e+" 3",value:"LOGICOP3"},{name:e+" 4",value:"LOGICOP4"}]}},{kind:"get",key:"_sourceTypes",value:function(){return[{name:this.lcn.localize("variables"),value:this._is2013?this._variablesNew:this._variablesOld,id:"variables"},{name:this.lcn.localize("setpoints"),value:this._setpoints,id:"setpoints"},{name:this.lcn.localize("thresholds"),value:this._is2013?this._thresholdsNew:this._thresholdsOld,id:"thresholds"},{name:this.lcn.localize("s0inputs"),value:this._s0Inputs,id:"s0inputs"},{name:this.lcn.localize("leds"),value:this._ledPorts,id:"ledports"},{name:this.lcn.localize("logics"),value:this._logicOpPorts,id:"logicopports"}]}},{kind:"get",key:"_varUnits",value:function(){return[{name:this.lcn.localize("unit-lcn-native"),value:"NATIVE"},{name:"Celsius",value:"°C"},{name:"Fahrenheit",value:"°F"},{name:"Kelvin",value:"K"},{name:"Lux",value:"LUX_T"},{name:"Lux (I-Port)",value:"LUX_I"},{name:this.lcn.localize("unit-humidity")+" (%)",value:"PERCENT"},{name:"CO2 (‰)",value:"PPM"},{name:this.lcn.localize("unit-wind")+" (m/s)",value:"METERPERSECOND"},{name:this.lcn.localize("unit-volts"),value:"VOLT"},{name:this.lcn.localize("unit-milliamperes"),value:"AMPERE"},{name:this.lcn.localize("unit-angle")+" (°)",value:"DEGREE"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,u.Z)(i.prototype),"connectedCallback",this).call(this),this._sourceType=this._sourceTypes[0],this._source=this._sourceType.value[0],this._unit=this._varUnits[0]}},{kind:"method",key:"render",value:function(){return this._sourceType||this._source?l.dy`
      <div class="sources">
        <ha-select
          id="source-type-select"
          .label=${this.lcn.localize("source-type")}
          .value=${this._sourceType.id}
          fixedMenuPosition
          @selected=${this._sourceTypeChanged}
          @closed=${d}
        >
          ${this._sourceTypes.map((e=>l.dy`
              <ha-list-item .value=${e.id}> ${e.name} </ha-list-item>
            `))}
        </ha-select>

        <ha-select
          id="source-select"
          .label=${this.lcn.localize("source")}
          .value=${this._source.value}
          fixedMenuPosition
          @selected=${this._sourceChanged}
          @closed=${d}
        >
          ${this._sourceType.value.map((e=>l.dy`
              <ha-list-item .value=${e.value}> ${e.name} </ha-list-item>
            `))}
        </ha-select>
      </div>

      <ha-select
        id="unit-select"
        .label=${this.lcn.localize("dashboard-entities-dialog-unit-of-measurement")}
        .value=${this._unit.value}
        fixedMenuPosition
        @selected=${this._unitChanged}
        @closed=${d}
      >
        ${this._varUnits.map((e=>l.dy` <ha-list-item .value=${e.value}> ${e.name} </ha-list-item> `))}
      </ha-select>
    `:l.Ld}},{kind:"method",key:"_sourceTypeChanged",value:function(e){const t=e.target;-1!==t.index&&(this._sourceType=this._sourceTypes.find((e=>e.id===t.value)),this._source=this._sourceType.value[0],this._sourceSelect.select(-1))}},{kind:"method",key:"_sourceChanged",value:function(e){const t=e.target;-1!==t.index&&(this._source=this._sourceType.value.find((e=>e.value===t.value)),this.domainData.source=this._source.value)}},{kind:"method",key:"_unitChanged",value:function(e){const t=e.target;-1!==t.index&&(this._unit=this._varUnits.find((e=>e.value===t.value)),this.domainData.unit_of_measurement=this._unit.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        .sources {
          display: grid;
          grid-template-columns: 1fr 1fr;
          column-gap: 4px;
        }
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `]}}]}}),l.oi),(0,a.Z)([(0,o.Mo)("lcn-config-switch-element")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"domainData",value(){return{output:"OUTPUT1"}}},{kind:"field",decorators:[(0,o.SB)()],key:"_portType",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_port",value:void 0},{kind:"field",decorators:[(0,o.IO)("#port-select")],key:"_portSelect",value:void 0},{kind:"get",key:"_outputPorts",value:function(){const e=this.lcn.localize("output");return[{name:e+" 1",value:"OUTPUT1"},{name:e+" 2",value:"OUTPUT2"},{name:e+" 3",value:"OUTPUT3"},{name:e+" 4",value:"OUTPUT4"}]}},{kind:"get",key:"_relayPorts",value:function(){const e=this.lcn.localize("relay");return[{name:e+" 1",value:"RELAY1"},{name:e+" 2",value:"RELAY2"},{name:e+" 3",value:"RELAY3"},{name:e+" 4",value:"RELAY4"},{name:e+" 5",value:"RELAY5"},{name:e+" 6",value:"RELAY6"},{name:e+" 7",value:"RELAY7"},{name:e+" 8",value:"RELAY8"}]}},{kind:"get",key:"_portTypes",value:function(){return[{name:this.lcn.localize("output"),value:this._outputPorts,id:"output"},{name:this.lcn.localize("relay"),value:this._relayPorts,id:"relay"}]}},{kind:"method",key:"connectedCallback",value:function(){(0,c.Z)((0,u.Z)(i.prototype),"connectedCallback",this).call(this),this._portType=this._portTypes[0],this._port=this._portType.value[0]}},{kind:"method",key:"render",value:function(){return this._portType||this._port?l.dy`
      <div id="port-type">${this.lcn.localize("port-type")}</div>

      <ha-formfield label=${this.lcn.localize("output")}>
        <ha-radio
          name="port"
          value="output"
          .checked=${"output"===this._portType.id}
          @change=${this._portTypeChanged}
        ></ha-radio>
      </ha-formfield>

      <ha-formfield label=${this.lcn.localize("relay")}>
        <ha-radio
          name="port"
          value="relay"
          .checked=${"relay"===this._portType.id}
          @change=${this._portTypeChanged}
        ></ha-radio>
      </ha-formfield>

      <ha-select
        id="port-select"
        .label=${this.lcn.localize("port")}
        .value=${this._port.value}
        fixedMenuPosition
        @selected=${this._portChanged}
        @closed=${d}
      >
        ${this._portType.value.map((e=>l.dy` <ha-list-item .value=${e.value}> ${e.name} </ha-list-item> `))}
      </ha-select>
    `:l.Ld}},{kind:"method",key:"_portTypeChanged",value:function(e){const t=e.target;this._portType=this._portTypes.find((e=>e.id===t.value)),this._port=this._portType.value[0],this._portSelect.select(-1)}},{kind:"method",key:"_portChanged",value:function(e){const t=e.target;-1!==t.index&&(this._port=this._portType.value.find((e=>e.value===t.value)),this.domainData.output=this._port.value)}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        #port-type {
          margin-top: 16px;
        }
        ha-select {
          display: block;
          margin-bottom: 8px;
        }
      `]}}]}}),l.oi);var h=i(1285);let m=(0,a.Z)([(0,o.Mo)("lcn-create-entity-dialog")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"lcn",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_name",value(){return""}},{kind:"field",decorators:[(0,o.SB)()],key:"domain",value(){return"binary_sensor"}},{kind:"field",decorators:[(0,o.SB)()],key:"_invalid",value(){return!0}},{kind:"get",key:"_domains",value:function(){return[{name:this.lcn.localize("binary-sensor"),domain:"binary_sensor"},{name:this.lcn.localize("climate"),domain:"climate"},{name:this.lcn.localize("cover"),domain:"cover"},{name:this.lcn.localize("light"),domain:"light"},{name:this.lcn.localize("scene"),domain:"scene"},{name:this.lcn.localize("sensor"),domain:"sensor"},{name:this.lcn.localize("switch"),domain:"switch"}]}},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this.lcn=e.lcn,this._name="",this._invalid=!0,await this.updateComplete}},{kind:"method",key:"render",value:function(){return this._params?l.dy`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        .heading=${(0,s.i)(this.hass,this.lcn.localize("dashboard-entities-dialog-create-title"))}
        @closed=${this._closeDialog}
      >
        <ha-select
          id="domain-select"
          .label=${this.lcn.localize("domain")}
          .value=${this.domain}
          fixedMenuPosition
          @selected=${this._domainChanged}
          @closed=${d}
        >
          ${this._domains.map((e=>l.dy`
              <ha-list-item .value=${e.domain}> ${e.name} </ha-list-item>
            `))}
        </ha-select>

        <ha-textfield
          id="name-input"
          label=${this.lcn.localize("entity-id")}
          type="string"
          prefix=${this.domain+"."}
          maxLength="20"
          @input=${this._nameChanged}
        ></ha-textfield>

        ${this.renderDomain(this.domain)}

        <div class="buttons">
          <mwc-button
            slot="secondaryAction"
            @click=${this._closeDialog}
            .label=${this.lcn.localize("dismiss")}
          ></mwc-button>
          <mwc-button
            slot="primaryAction"
            .disabled=${this._invalid}
            @click=${this._create}
            .label=${this.lcn.localize("create")}
          ></mwc-button>
        </div>
      </ha-dialog>
    `:l.Ld}},{kind:"method",key:"renderDomain",value:function(e){if(!this._params)return l.Ld;switch(e){case"binary_sensor":return l.dy`<lcn-config-binary-sensor-element
          id="domain"
          .hass=${this.hass}
          .lcn=${this.lcn}
        ></lcn-config-binary-sensor-element>`;case"climate":return l.dy`<lcn-config-climate-element
          id="domain"
          .hass=${this.hass}
          .lcn=${this.lcn}
          .softwareSerial=${this._params.device.software_serial}
          @validity-changed=${this._validityChanged}
        ></lcn-config-climate-element>`;case"cover":return l.dy`<lcn-config-cover-element
          id="domain"
          .hass=${this.hass}
          .lcn=${this.lcn}
        ></lcn-config-cover-element>`;case"light":return l.dy`<lcn-config-light-element
          id="domain"
          .hass=${this.hass}
          .lcn=${this.lcn}
          @validity-changed=${this._validityChanged}
        ></lcn-config-light-element>`;case"scene":return l.dy`<lcn-config-scene-element
          id="domain"
          .hass=${this.hass}
          .lcn=${this.lcn}
          @validity-changed=${this._validityChanged}
        ></lcn-config-scene-element>`;case"sensor":return l.dy`<lcn-config-sensor-element
          id="domain"
          .hass=${this.hass}
          .lcn=${this.lcn}
          .softwareSerial=${this._params.device.software_serial}
        ></lcn-config-sensor-element>`;case"switch":return l.dy`<lcn-config-switch-element
          id="domain"
          .hass=${this.hass}
          .lcn=${this.lcn}
        ></lcn-config-switch-element>`;default:return l.Ld}}},{kind:"method",key:"_nameChanged",value:function(e){const t=e.target;this._name=t.value,this._validityChanged(new CustomEvent("validity-changed",{detail:!this._name}))}},{kind:"method",key:"_validityChanged",value:function(e){this._invalid=e.detail}},{kind:"method",key:"_create",value:async function(){var e;const t=null===(e=this.shadowRoot)||void 0===e?void 0:e.querySelector("#domain"),i={name:this._name?this._name:this.domain,address:this._params.device.address,domain:this.domain,domain_data:t.domainData};await this._params.createEntity(i)?this._closeDialog():await(0,h.Ys)(this,{title:this.lcn.localize("dashboard-entities-dialog-add-alert-title"),text:`${this.lcn.localize("dashboard-entities-dialog-add-alert-text")}\n              ${this.lcn.localize("dashboard-entities-dialog-add-alert-hint")}`})}},{kind:"method",key:"_closeDialog",value:function(){this._params=void 0,(0,n.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"_domainChanged",value:function(e){const t=e.target;this.domain=t.value}},{kind:"get",static:!0,key:"styles",value:function(){return[r.yu,l.iv`
        ha-dialog {
          --mdc-dialog-max-width: 500px;
          --dialog-z-index: 10;
        }
        ha-select,
        ha-textfield {
          display: block;
          margin-bottom: 8px;
        }
        .buttons {
          display: flex;
          justify-content: space-between;
          padding: 8px;
        }
      `]}}]}}),l.oi)}};
//# sourceMappingURL=ovjKXg0y.js.map