package com.logitics.erp.position.repository;

import com.logitics.erp.position.entity.Position;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface PositionRepository extends JpaRepository<Position, Long> {
    Optional<Position> findByPositionName(String positionName);
}
