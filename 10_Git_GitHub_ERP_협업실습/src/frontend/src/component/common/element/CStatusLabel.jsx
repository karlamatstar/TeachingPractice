import c from './CStatusLabel.module.css';

export default function CStatusLabel({type, labelName}) {
  return (
    <span className={`${c.statusLabel} ${ type === 'type1' ? c.type1 : c.type2}`}>
      {labelName}
    </span>
  )

}