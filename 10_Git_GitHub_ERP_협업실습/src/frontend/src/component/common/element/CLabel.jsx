import s from './CLabel.module.css'

export default function CLabel({labelName}) {
    return (
        <span className={s.labelName}>{labelName}</span>
    )
}