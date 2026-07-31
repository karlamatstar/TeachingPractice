import c from './CInputCustom.module.css';

export default function CInputCustom({labelName, beforeIcon, iconColor = '#9CA3AF', inputType = 'text', placeholder, afterIcon}) {
  return (
    <div className={c.inputItem}>
      <span className={c.beforeIcon}>
        {beforeIcon}
      </span>
      <label>{labelName}</label>
      <input type={inputType} placeholder={placeholder}
        className={beforeIcon ? c.inputPadding : c.normalPadding}
      />
      <span className={c.afterIcon}>
        {afterIcon}
      </span>
    </div>
  )
}