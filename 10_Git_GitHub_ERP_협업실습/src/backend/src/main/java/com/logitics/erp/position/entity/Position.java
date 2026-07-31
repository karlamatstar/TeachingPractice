package com.logitics.erp.position.entity;

import com.logitics.erp.common.entity.BaseEntity;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Table(name = "positions")
public class Position extends BaseEntity {

	public Position(String positionName, Integer positionLevel) {
		this.positionName = positionName;
		this.positionLevel = positionLevel;
	}

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long positionId;

	@Column(nullable = false)
	private String positionName;

	@Column(unique = true)
	private Integer positionLevel;

}
