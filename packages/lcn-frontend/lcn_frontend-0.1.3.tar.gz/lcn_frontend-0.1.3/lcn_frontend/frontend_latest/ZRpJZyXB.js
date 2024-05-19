export const id=942;export const ids=[942];export const modules={1942:(i,e,o)=>{o.r(e),o.d(e,{ProgressDialog:()=>l});var t=o(309),a=(o(7006),o(8144)),s=o(4243),d=o(9950),r=o(8394);let l=(0,t.Z)([(0,s.Mo)("progress-dialog")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.IO)("ha-dialog",!0)],key:"_dialog",value:void 0},{kind:"method",key:"showDialog",value:async function(i){this._params=i,await this.updateComplete,(0,r.B)(this._dialog,"iron-resize")}},{kind:"method",key:"closeDialog",value:async function(){this.close()}},{kind:"method",key:"render",value:function(){var i,e;return this._params?a.dy`
      <ha-dialog open scrimClickAction escapeKeyAction @close-dialog=${this.closeDialog}>
        <h2>${null===(i=this._params)||void 0===i?void 0:i.title}</h2>
        <p>${null===(e=this._params)||void 0===e?void 0:e.text}</p>

        <div id="dialog-content">
          <ha-circular-progress active></ha-circular-progress>
        </div>
      </ha-dialog>
    `:a.Ld}},{kind:"method",key:"close",value:function(){this._params=void 0}},{kind:"get",static:!0,key:"styles",value:function(){return[d.yu,a.iv`
        #dialog-content {
          text-align: center;
        }
      `]}}]}}),a.oi)}};
//# sourceMappingURL=ZRpJZyXB.js.map