package com.logitics.erp.position;

import com.logitics.erp.position.entity.Position;
import com.logitics.erp.position.mapper.PositionMapper;
import com.logitics.erp.position.repository.PositionRepository;
import lombok.Getter;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
public class PositionServiceTests {

	@Autowired
	private PositionMapper positionMapper;

	@Autowired
	private PositionRepository positionRepository;

	@Test
	public void createPositions() {

		List<Position> positions = List.of(
						new Position("임원", 6),
						new Position("부장", 5),
						new Position("차장", 4),
						new Position("과장", 3),
						new Position("대리", 2),
						new Position("사원", 1)
		);

		positionRepository.saveAll(positions);

	}

}
